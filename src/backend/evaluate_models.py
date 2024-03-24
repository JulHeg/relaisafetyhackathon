import json
from collections import Counter
import argparse

parser = argparse.ArgumentParser(description='Choose the AI model for evaluation.')
parser.add_argument('--model', type=str, choices=['gpt-4', 'gpt-3.5-turbo', "claude-3-sonnet", "llama-7b-chat"], required=True, help='The AI model to use')
args = parser.parse_args()
with open(f'results/{args.model}_responses.json', 'r') as file:
    data = json.load(file)

group_size = 18
total_groups = len(data) // group_size
correct_majority_votes = 0
individual_accuracies = []
majority_votes_per_group = []
confidences = []

# Process each group of 18 questions
for i in range(0, len(data), group_size):
    group = data[i:i+group_size]

    # Count the occurrences of each model response
    correct_answer = group[0]["options"][group[0]['correct_answer'] - 1]
    answers = [item['model_response'] for item in group]
    answers = [item["options"][int(answer) - 1] if answer.isdigit() else None for answer, item in zip(answers, group)]

    response_counts = Counter(answers)

    majority_vote, count = response_counts.most_common(1)[0]

    majority_votes_per_group.append(majority_vote)
    confidences.append(count / len(group))

    # Calculate the accuracy for this group
    group_correct_answers = response_counts[correct_answer]
    group_accuracy = (group_correct_answers / len(group)) * 100
    individual_accuracies.append(group_accuracy)

    # Check if the majority vote is the correct answer and increment correct_majority_votes if it is
    if majority_vote and (majority_vote == correct_answer):
        correct_majority_votes += 1

# Calculate the overall accuracy based on the majority votes
majority_vote_accuracy = (correct_majority_votes / total_groups) * 100

# Calculate the mean of individual accuracies
mean_accuracy = sum(individual_accuracies) / total_groups

# Prepare the results in a dictionary
results = {
    "Total Groups": total_groups,
    "Correct Majority Votes": correct_majority_votes,
    "Majority Vote Accuracy": majority_vote_accuracy,
    "Mean Accuracy": mean_accuracy,
    "Individual Accuracies": individual_accuracies,
    "Majority Votes Per Group": majority_votes_per_group,
    "Confidences": confidences
}

# Save the results to a file in a pretty format
with open(f'results/{args.model}_results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

print("Results saved to file.")
