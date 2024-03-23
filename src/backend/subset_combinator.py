import json

file_path_original = '../../data/raw_data/random_subset.json'
file_path_rephrased = '../../data/raw_data/random_subset_rephrased.json'


def read_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        data=json.load(file)
    return data


data_original=read_jsonl_file(file_path_original)
data_rephrased=read_jsonl_file(file_path_rephrased)
data_combined=[]
#Combine the json files
for i,object in enumerate(data_original):
    data = data_rephrased[i]
    for key in object.keys():
        data[key]=object[key]
    data_combined.append(data)

# Path for the modified data file
modified_file_path = '../../data/random_subset_rephrased_combined.json'  # Replace with your desired path

# Write the modified data back to a file
with open(modified_file_path, 'w') as file:
    json.dump(data_combined, file, indent=4)
