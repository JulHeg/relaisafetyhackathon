import json
from collections import Counter

# Load the JSON data from a file
with open('results/openai_responses.json', 'r') as file:
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
    # Find the majority vote ensuring it's an integer
    majority_vote = None
    for response, count in response_counts.most_common():
        # Check if the response is an integer
        if response:
            majority_vote = response
            confidences.append(count / len(group))
            break
    if majority_vote:
        majority_votes_per_group.append(majority_vote)
    else:
        majority_votes_per_group.append(None)
        confidences.append(0)

    # Calculate the accuracy for this group
    group_correct_answers = response_counts[correct_answer]
    group_accuracy = (group_correct_answers / len(group)) * 100
    individual_accuracies.append(group_accuracy)

    # Check if the majority vote is the correct answer and increment correct_majority_votes if it is
    if majority_vote and (majority_vote == correct_answer):
        correct_majority_votes += 1
        # print(majority_vote)
    else:
        print(majority_vote)

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
    "Confidences": confidences  # Convert Counter to dict for JSON serialization
}

# Save the results to a file in a pretty format
with open('results/results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

print("Results saved to results.json")
