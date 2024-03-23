import argparse
import json
import os
from dotenv import load_dotenv
import openai
import anthropic
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from openai import RateLimitError
import itertools

# Initialize argparse to accept command line arguments
parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['openai', 'anthropic'], required=True, help='The AI model to use: openai or anthropic')
args = parser.parse_args()

load_dotenv()

claude_api_key = os.environ.get('CLAUDE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

openai_client = openai.OpenAI(api_key=openai_api_key)
anthropic_client = anthropic.Anthropic(api_key=claude_api_key)

@retry(
    wait=wait_fixed(5),  # Wait 60 seconds before retrying
    stop=stop_after_attempt(5),  # Stop after 5 attempts
    retry=retry_if_exception_type(RateLimitError)  # Retry only on RateLimitError
)
def get_response(prompt, model):
    if model == 'openai':
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            seed=42,
            max_tokens=32,
            stop=["."],
        )
        return completion.choices[0].message.content.strip()
    elif model == 'anthropic':
        message = anthropic_client.messages.create(
            # model="claude-3-opus-20240229",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=32,
            stop_sequences=["1", "2", "3"],
        )
        return message.stop_sequence

with open('data/random_subset_rephrased_combined.json') as file:
    dataset = json.load(file)

with open('data/random_subset_rephrased_combined.lst', 'r') as file:
    correct_labels = [int(line.strip()) for line in file.readlines()]

results = []
instruction_text = "You are taking a multiple choice test. You will be shown a context and a question, followed by numbered multiple choice answers. Respond with the number corresponding to the correct answer."

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
            response = get_response(prompt, args.model)

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

with open('results/gpt-3.5-turbo_responses.json', 'w') as file:
    json.dump(results, file, indent=2)
