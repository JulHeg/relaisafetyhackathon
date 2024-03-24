import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import random
    
st.set_page_config(page_title='MindMatch', page_icon='🧪', layout="centered", menu_items=None, initial_sidebar_state='collapsed')

st.sidebar.image(os.path.join('src', 'frontend', 'MindMatch-Logo_Horizontal.png'), width=300)
st.sidebar.markdown("""The Social-IQ dataset stands as a pioneering benchmark tailored for the training and assessment of socially intelligent technologies. Rooted in the recognition of social intelligence as a crucial component for intelligent systems to effectively interpret human intents and facilitate rich interactions, Social-IQ diverges from traditional numeric-based social modeling approaches by leveraging an unconstrained methodology.

Despite humans showcasing a high accuracy rate of 95.08% in reasoning about these social scenarios, current state-of-the-art computational models lag significantly. The benchmark encompasses wide array of real-world social interactions, from casual gatherings to more formal events, and providing a diverse set of questions aimed at probing different aspects of social intelligence.
""")
st.title('Social-IQ Benchmark')

random_subset_path = os.path.join('data', 'raw_data', 'random_subset.json')
random_subset_label_path = os.path.join('data', 'raw_data', 'random_subset_labels_rephrased.lst')
with open(random_subset_path) as f:
    questions_subset = json.load(f)
with open(random_subset_label_path) as f:
    questions_labels = f.readlines()
questions_answers = []
model_answer_paths = {
    'GPT-4': os.path.join('results', 'gpt-4_results.json'),
    'GPT-3.5': os.path.join('results', 'gpt-3.5-turbo_results.json')
}
model_answers = {}
for model, path in model_answer_paths.items():
    with open(path) as f:
        model_answers[model] = json.load(f)


for i in range(len(questions_subset)):
    question = questions_subset[i]
    llm_answers = {}
    answer_possibilites = [question['answerA'], question['answerB'], question['answerC']]
    for model, answers in model_answers.items():
        answer = answers['Majority Votes Per Group'][i]
        if answer not in answer_possibilites:
            print(f"Answer not found: {answer}")
            print(answers['Majority Votes Per Group'][i])
            chatgpt_answer_index = len(answer_possibilites)
        else:
            chatgpt_answer_index = answer_possibilites.index(answer) 
        llm_answers[model] = {
            'answer': chatgpt_answer_index,
            'confidence': answers['Confidences'][i],
                'explanation': 'Answer elaboration B'
        }
    qa = {
        'question': question['context'] + ' ' + question['question'],
        'answers': answer_possibilites,
        'correct_answer': int(questions_labels[i].strip()) - 1,
        'llm_answers': llm_answers
    }
    #print(qa)
    questions_answers.append(qa)
question_count = len(questions_answers)

# Keep track of the answered questions in the session state

if 'answers_given' not in st.session_state:
    st.session_state.answers_given = []
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

for i, qa in enumerate(questions_answers):
    # If one of the previous questions has not been answered, continue to the next question
    if st.session_state.question_index != i:
        continue
        
    st.subheader(f'Question {i+1}/{question_count}: ' + qa['question'])
    option = st.radio(
        "Choose your answer:",
        qa['answers'] + ["Not enough information"],
        key=f'question_{i}',
        disabled=len(st.session_state.answers_given) > i
    )
    submitted = st.button('Check', key=f'submit_{i}', 
                          #disabled=st.session_state.answered_questions[i]
                          )
    correct_answer = qa['answers'][qa['correct_answer']]
    if submitted:
        # Make a 'Next' button to go to the next question
        st.session_state.answers_given.append(option)
        st.rerun()
    if len(st.session_state.answers_given) > i:
        # Disable the button after submission
        if option == correct_answer:
            st.write("Correct!")
        else:
            st.write(f"Incorrect answer: {correct_answer}")
        
        for model, model_answer in qa['llm_answers'].items():
            if model_answer['answer'] == len(qa['answers']):
                given_answer = "Not enough information"
            else:
                given_answer = qa['answers'][model_answer['answer']]
            confidence = model_answer['confidence']
            with st.expander(f"{model} answer: {given_answer} (Confidence: {int(confidence*100)}%)", expanded=False):
                st.write(model_answer['explanation'])
        next = st.button('Next', key=f'next_{i}')   
        if next:
            # Update to remove the old question
            st.session_state.question_index += 1
            st.rerun()
            pass
            
                
# Once all questions are answered, show the final score
if st.session_state.question_index == question_count:
    correct_answers = 0
    for i, qa in enumerate(questions_answers):
        if st.session_state.answers_given[i] == qa['answers'][qa['correct_answer']]:
            correct_answers += 1
    st.write("Quiz completed!")
    st.write(f"Final score: {correct_answers}/{len(questions_answers)}")

    
    # Calculate the accuracy of all the LLMs
    llms_correct_answers = {}
    for qa in questions_answers:
        for model, model_answer in qa['llm_answers'].items():
            if model not in llms_correct_answers:
                llms_correct_answers[model] = 0
            if model_answer['answer'] == qa['correct_answer']:
                llms_correct_answers[model] += 1
                
    # Plot a bar chart of the accuracy of all the LLMs and the user
    user_accuracy = correct_answers / len(questions_answers)
    llms_accuracy = {model: correct_answers / len(questions_answers) for model, correct_answers in llms_correct_answers.items()}
    llms_accuracy['User'] = user_accuracy
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()

    # Create the bar chart
    bars = ax.bar(llms_accuracy.keys(), llms_accuracy.values(), color='skyblue')

    # Set the title and labels
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Compare Your Accuracy to the LLMs', fontsize=14, fontweight='bold')

    # Improve readability of x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Set the y-axis limits
    ax.set_ylim(0, 1)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Streamline the presentation
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Display the plot
    st.pyplot(fig)
    st.write("The bar chart above shows the accuracy of the user and the LLMs on the Social-IQ benchmark. Note that the question presented here are from real LLM Benchmarks that usually get crowdsourced questions and answers. They can sometimes be tricky or ambiguous.")
    st.page_link("Home.py", label="Go back to the main page", icon="🧪")