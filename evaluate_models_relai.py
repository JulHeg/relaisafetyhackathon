import json
from collections import Counter
import argparse

parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['gpt-4', 'gpt-3.5-turbo', "claude-3-sonnet"], required=True, help='The AI model to use')
args = parser.parse_args()
with open(f'results/{args.model}_relai_responses.json', 'r') as file:
    data = json.load(file)

group_size = 120
total_groups = len(data) // group_size
majority_votes_per_group = []
confidences = []

# Process each group of 5 questions
for i in range(0, len(data), group_size):
    group = data[i:i+group_size]

    # Count the occurrences of each model response
    answers = [item['model_response'] for item in group]
    answers = [item["options"][int(answer) - 1] if answer.isdigit() else None for answer, item in zip(answers, group)]

    response_counts = Counter(answers)

    majority_vote, count = response_counts.most_common(1)[0]

    majority_votes_per_group.append(majority_vote)
    confidences.append(count / len(group))



# Prepare the results in a dictionary
results = {
    "Total Groups": total_groups,
    "Majority Votes Per Group": majority_votes_per_group,
    "Confidences": confidences
}

# Save the results to a file in a pretty format
with open(f'results/{args.model}_relai_results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

print("Results saved to file.")
