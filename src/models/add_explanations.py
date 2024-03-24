import argparse
import json
import os
from dotenv import load_dotenv
import openai
import anthropic
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from openai import RateLimitError

# Initialize argparse to accept command line arguments
parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['gpt-4', 'gpt-3.5-turbo'], required=True, help='The AI model to use')
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
def get_explanation(prompt, answer):
    if args.model in ['gpt-4', 'gpt-3.5-turbo']:
        completion = openai_client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
                {"role": "user", "content": "Give a brief and concise explanation for your answer."},
            ],
            temperature=0.0,
            seed=42,
            max_tokens=128,
        )
        return completion.choices[0].message.content.strip()
    elif args.model in ['claude-3-sonnet']:
        message = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
                {"role": "user", "content": "Give a brief and concise explanation for your answer."},
            ],
            temperature=0.0,
            max_tokens=128,
        )
        return message.content[0].text.strip()
    else:
        NotImplementedError(f"Model {args.model} not implemented")

with open(f'results/{args.model}_responses.json') as file:
    dataset = json.load(file)

with open(f'results/{args.model}_results.json', 'r') as file:
    answers = json.load(file)
    answers = answers["Majority Votes Per Group"]

results = []
for index, item in enumerate(dataset):
    current_question = index // 18

    if any(result['id'] == current_question for result in results):
        continue
    print(f"Processing question {current_question}...")
    
    majority_vote = answers[current_question]
    
    response = item["model_response"]
    if response.isdigit():
        answer = item["options"][int(response)-1]
    else:
        answer = None

    if answer != majority_vote:
        continue

    prompt = item["prompt"]
    explanation = get_explanation(prompt, item["model_response"])

    # Store the result for this permutation
    result = {
        'id': current_question,
        'explanation': explanation,
        'majority_answer': majority_vote,
    }
    results.append(result)

with open(f'results/{args.model}_explanations.json', 'w') as file:
    json.dump(results, file, indent=2)

