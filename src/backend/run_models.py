import argparse
import json
import os
from dotenv import load_dotenv
import openai
import anthropic
from tenacity import retry, retry_any, wait_fixed, stop_after_attempt, retry_if_exception_type
import itertools
import replicate

# Initialize argparse to accept command line arguments
parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['gpt-4', 'gpt-3.5-turbo', "claude-3-sonnet", "llama-7b-chat"], required=True, help='The AI model to use')
args = parser.parse_args()

load_dotenv()

claude_api_key = os.environ.get('CLAUDE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

openai_client = openai.OpenAI(api_key=openai_api_key)
anthropic_client = anthropic.Anthropic(api_key=claude_api_key)

@retry(
    wait=wait_fixed(10),  # Wait 60 seconds before retrying
    stop=stop_after_attempt(5),  # Stop after 5 attempts
    retry=retry_any(
        retry_if_exception_type(openai.RateLimitError),
        retry_if_exception_type(anthropic.RateLimitError)
    )
)
def get_response(prompt):
    if args.model in ['gpt-4', 'gpt-3.5-turbo']:
        completion = openai_client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            seed=42,
            max_tokens=32,
            stop=["."],
        )
        return completion.choices[0].message.content.strip()
    elif args.model in ['claude-3-sonnet']:
        message = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=32,
            stop_sequences=["1", "2", "3"],
        )
        if message.stop_reason == "stop_sequence":
            return message.stop_sequence
        else:
            return message.content[0].text.strip()
    elif args.model == 'llama-7b-chat':
        system = prompt.split("\n\n")[0]
        user = "\n\n".join(prompt.split("\n\n")[1:])
        message = replicate.run(
            "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
            input={
                "seed": 42,
                "debug": False,
                "prompt": user,
                "system_prompt": system,
                "temperature": 0.01,
                "max_new_tokens": 64,
                "repetition_penalty": 1.0,
                "stop_sequences": "</s>"
            }
        )
        output = ''.join(message)
        if "1" in output:
            return "1"
        elif "2" in output:
            return "2"
        elif "3" in output:
            return "3"
        else:
            return output
    else:
        NotImplementedError(f"Model {args.model} not implemented")

with open('data/random_subset_rephrased_combined.json') as file:
    dataset = json.load(file)

with open('data/random_subset_rephrased_combined.lst', 'r') as file:
    correct_labels = [int(line.strip()) for line in file.readlines()]

results = []
instruction_text = "You will be shown a context and a question, followed by numbered multiple choice answers. Respond with the number corresponding to the best answer. If you don't know or you think there is not enough information, give your best guess."

for index, item in enumerate(dataset):
    print(f"{index + 1}/{len(dataset)}")
    for context in [item["context"], item['context_2'], item['context_3']]:
        question = item['question']
        options = [item['answerA'], item['answerB'], item['answerC']]
        correct_answer = options[int(correct_labels[index])-1]

        # Generate all permutations of the options
        for permutation in itertools.permutations(options):
            prompt = f"{instruction_text}\n\nContext: {context}\nQuestion: {question}\n"
            for idx, option in enumerate(permutation):
                prompt += f"{idx + 1}. {option}\n"
            prompt += "\nCorrect Answer:"

            # Call the model with the shuffled options
            response = get_response(prompt)

            # Store the result for this permutation
            result = {
                'context': context,
                'question': question,
                'prompt': prompt,
                'options': permutation,
                'correct_answer': permutation.index(correct_answer) + 1,
                'model_response': response,
            }
            results.append(result)

with open(f'results/{args.model}_responses.json', 'w') as file:
    json.dump(results, file, indent=2)
