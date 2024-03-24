import argparse
import json
import os
from dotenv import load_dotenv
import openai
import anthropic
from tenacity import retry, retry_any, wait_fixed, stop_after_attempt, retry_if_exception_type
import itertools

# Initialize argparse to accept command line arguments
parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['gpt-4', 'gpt-3.5-turbo', "claude-3-sonnet"], required=True, help='The AI model to use')
#python run_models_relai.py --model gpt-3.5-turbo
args = parser.parse_args()

load_dotenv()

# claude_api_key = os.environ.get('CLAUDE_API_KEY')
# openai_api_key = os.environ.get('OpenAI_API_KEY')

openai_client = openai.OpenAI(api_key='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')
anthropic_client = None#anthropic.Anthropic(api_key=claude_api_key)
print("APIs initialized")
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
    else:
        NotImplementedError(f"Model {args.model} not implemented")

with open('data/relai_questions.json') as file:
    dataset = json.load(file)

# with open('data/random_subset_rephrased_combined.lst', 'r') as file:
#     correct_labels = [int(line.strip()) for line in file.readlines()]

results = []
instruction_text = "You will be shown a context and a question, followed by numbered multiple choice answers. Respond with the number corresponding to the best answer. If you don't know or you think there is not enough information, give your best guess."

for index, item in enumerate(dataset):
    print(f"{index + 1}/{len(dataset)}")
    for context in [item["context"]]:
        question = item['question']
        options = [item['answerA'], item['answerB'], item['answerC'], item['answerD'], item['answerE']]
        # correct_answer = options[int(correct_labels[index])-1]

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
                'model_response': response,
            }
            results.append(result)

with open(f'results/{args.model}_relai_responses.json', 'w') as file:
    json.dump(results, file, indent=2)
