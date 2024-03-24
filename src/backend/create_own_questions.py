import json
import random

def read_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        data=json.load(file)
    return data

def replace_pronouns(text, gender):
    if gender=="female":
        text = text.replace("{him/her}", "her")
        text = text.replace("{his/her}", "her")
        text = text.replace("{His/Her}", "Her")
        text = text.replace("{he/she}", "she")
        text = text.replace("{himself/herself}", "herself")
    elif gender=="male":
        text = text.replace("{him/her}", "him")
        text = text.replace("{His/Her}", "His")
        text = text.replace("{his/her}", "his")
        text = text.replace("{he/she}", "he")
        text = text.replace("{himself/herself}", "himself")
    return text

def create_new_data(questions,scenarios,seed=None):
    #Create new data
    new_data=[]
    if seed!=None:
        random.seed(10)
    letters=["A","B","C","D","E","F"]
    for i, question in enumerate(questions):
        new_question={}
        #Get random choice
        female_name = random.choice(scenarios[i]["female_name"])
        male_name = random.choice(scenarios[i]["male_name"])
        scenario = random.choice(scenarios[i]["scenarios"])
        random_adjectives = random.sample(scenarios[i]["adjectives"], 5)

        context = question["context"].replace("{female_name}", female_name)
        context = context.replace("{male_name}", male_name)
        context = context.replace("{scenario}", scenario)

        question = question["question"].replace("{female_name}", female_name)

        if "gender" in scenarios[i].keys():
            gender = random.choice(scenarios[i]["gender"])
            name = random.choice(scenarios[i][f"{gender}_name"])
            context = context.replace("{name}", name)
            context = replace_pronouns(context, gender)
            

        new_question["context"]=context
        new_question["question"]=question
        for i,adjective in enumerate(random_adjectives):
            new_question[f"answer{letters[i]}"]=adjective
        new_data.append(new_question)

    return new_data

#Read data
file_path_questions = '../../data/raw_data/relai_questions.json'
file_path_scenarios = '../../data/raw_data/relai_scenarios.json'

questions = read_jsonl_file(file_path_questions)
scenarios = read_jsonl_file(file_path_scenarios)


new_data=create_new_data(questions,scenarios)
#Save data
modified_file_path = '../../data/relai_questions.json'  # Replace with your desired path


# Write the modified data back to a file
with open(modified_file_path, 'w') as file:
    json.dump(new_data, file, indent=4)