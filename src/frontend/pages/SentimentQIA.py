import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import time
    
st.set_page_config(page_title='MindMatch', page_icon='🧪', layout="centered", menu_items=None)

st.sidebar.image(os.path.join('src', 'frontend', 'MindMatch-Logo_Horizontal.png'), width=300)
st.sidebar.markdown("""The Social-IQ dataset stands as a pioneering benchmark tailored for the training and assessment of socially intelligent technologies. Rooted in the recognition of social intelligence as a crucial component for intelligent systems to effectively interpret human intents and facilitate rich interactions, Social-IQ diverges from traditional numeric-based social modeling approaches by leveraging an unconstrained methodology.

Despite humans showcasing a high accuracy rate of 95.08% in reasoning about these social scenarios, current state-of-the-art computational models lag significantly. The benchmark encompasses wide array of real-world social interactions, from casual gatherings to more formal events, and providing a diverse set of questions aimed at probing different aspects of social intelligence.
""")
st.title('SentimentQIA')
model_images = {
    'GPT-4': os.path.join('src', 'frontend', 'gpt-4.jpg'),
    'GPT-3.5': os.path.join('src', 'frontend', 'gpt-3.5.png')
}
random_subset_path = os.path.join('data', 'relai_questions.json')
with open(random_subset_path) as f:
    questions_subset = json.load(f)
questions_answers = []
model_answer_paths = {
    'GPT-3.5': os.path.join('results', 'gpt-3.5-turbo_relai_results.json'),
    'GPT-4': os.path.join('results', 'gpt-4_relai_results.json'),
}
model_answers = {}
for model, path in model_answer_paths.items():
    with open(path) as f:
        model_answers[model] = json.load(f)
        
model_explanation_paths = {
    'GPT-3.5': os.path.join('results', 'gpt-3.5-turbo_relai_explanations.json'),
    'GPT-4': os.path.join('results', 'gpt-4_relai_explanations.json'),
}
model_explanations = {}
for model, path in model_explanation_paths.items():
    with open(path) as f:
        model_explanations[model] = json.load(f)
        


for i in range(len(questions_subset)):
    question = questions_subset[i]
    llm_answers = {}
    answer_possibilites = [question['answerA'], question['answerB'], question['answerC'], question['answerD'], question['answerE']]
    for model, answers in model_answers.items():
        answer = answers['Majority Votes Per Group'][i]
        if answer not in answer_possibilites:
            chatgpt_answer_index = -1
        else:
            chatgpt_answer_index = answer_possibilites.index(answer) 
        explanations = model_explanations[model]
        # Get the explanation where 'id' is i
        explanation = next((explanation for explanation in explanations if explanation['id'] == i), None)
        if explanation:
            explanation = explanation['explanation']
        else:
            explanation = 'No explanation available'
        llm_answers[model] = {
            'answer': chatgpt_answer_index,
            'confidence': answers['Confidences'][i],
                'explanation': explanation
        }
    question_text = " ".join([question['context'], question['question']])
    qa = {
        'question': question_text,
        'answers': answer_possibilites,
        'llm_answers': llm_answers
    }
    questions_answers.append(qa)
question_count = len(questions_answers)

# Keep track of the answered questions in the session state

if 'answers_given' not in st.session_state:
    st.session_state.answers_given = []
if 'question_index' not in st.session_state:
    st.session_state.question_index = -1
    
def stream_text(text):
    time.sleep(1.3)
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

if st.session_state.question_index == -1:
    st.write("Welcome to the Social-IQ Benchmark! This benchmark is designed to test the social intelligence of language models by presenting them with a series of social scenarios and questions. Here you can try it yourself and compare your answers with those of different popular language models. You will be asked to choose the most appropriate response to each scenario.")
    next = st.button('Start the quiz', key=f'next_{st.session_state.question_index}')
    if next:
        st.session_state.question_index += 1
        st.rerun()  

for i, qa in enumerate(questions_answers):
    # If one of the previous questions has not been answered, continue to the next question
    if st.session_state.question_index != i:
        continue
        
    st.subheader(f'Question {i+1}/{question_count}: ' + qa['question'])
    option = st.radio(
        "Choose your answer:",
        qa['answers'],
        key=f'question_{i}',
        disabled=len(st.session_state.answers_given) > i
    )
    submitted = st.button('Check', key=f'submit_{i}', 
                          #disabled=st.session_state.answered_questions[i]
                          )
    if submitted:
        # Make a 'Next' button to go to the next question
        st.session_state.answers_given.append(option)
        st.rerun()
    if len(st.session_state.answers_given) > i:
        # Disable the button after submission
        for model, model_answer in qa['llm_answers'].items():
            if model_answer['answer'] == len(qa['answers']):
                given_answer = "Not enough information"
            else:
                given_answer = qa['answers'][model_answer['answer']]
            confidence = model_answer['confidence']
            with st.expander(f"{model} answer: {given_answer} (Confidence: {int(confidence*100)}%)", expanded=False):
                with st.chat_message(model, avatar=model_images[model]):
                    st.write(model_answer['explanation'])
                    # st.write_stream(stream_text(model_answer['explanation'])) too buggy
        next = st.button('Next', key=f'next_{i}')   
        if next:
            # Update to remove the old question
            st.session_state.question_index += 1
            st.rerun()
            pass
            
                
# Once all questions are answered, show the final score

if st.session_state.question_index == question_count:
    st.write("You have answered all the questions! Thank you for playing!")
    quit()
    # Count up how often the different models agreed with the user
    agreement_counts = {}
    for i, qa in enumerate(questions_answers):
        answer_user = st.session_state.answers_given[i]
        for model, model_answer in qa['llm_answers'].items():
            if model_answer['answer'] == qa['answers'].index(answer_user):
                if model not in agreement_counts:
                    agreement_counts[model] = 0
                agreement_counts[model] += 1
    st.write("Agreement with your answers:")
    for model, count in agreement_counts.items():
        st.write(f"{model}: {count}/{question_count}")
    
    
    correct_answers = 0
    for i, qa in enumerate(questions_answers):
        if st.session_state.answers_given[i] == qa['answers'][qa['correct_answer']]:
            correct_answers += 1
    st.write("Quiz completed!")
    st.write(f"Final score: {correct_answers}/{len(questions_answers)}")

    
    # Calculate the accuracy of all the LLMs
    llms_correct_answers = {}
    llms_nonanswers = {}
    llms = list(model_answers.keys())
    for model in llms:
        llms_correct_answers[model] = 0
        llms_nonanswers[model] = 0
    print(questions_answers)
    for qa in questions_answers:
        for model, model_answer in qa['llm_answers'].items():
            if model_answer['answer'] == qa['correct_answer']:
                llms_correct_answers[model] += 1
            if model_answer['answer'] == -1:
                llms_nonanswers[model] += 1
    # print(llms_nonanswers)
    # Plot a bar chart of the accuracy of all the LLMs and the user
    # user_accuracy = correct_answers / len(questions_answers)
    # llms_accuracy = {model: correct_answers / len(questions_answers) for model, correct_answers in llms_correct_answers.items()}
    # llms_accuracy['User'] = user_accuracy
    # plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()

    list_of_accurate_responses = [correct_answers] + [llms_correct_answers[model] for model in llms]
    list_of_nonanswers = [0] + [llms_nonanswers[model] for model in llms]
    # Add them element-wise
    list_of_accurate_or_nonresponses = [sum(x) for x in zip(list_of_accurate_responses, list_of_nonanswers)]
    print(list_of_accurate_responses)
    print(list_of_accurate_or_nonresponses)
    #bars = ax.bar(llms_accuracy.keys(), llms_accuracy.values(), color='skyblue')
    bars = ax.bar(['You'] + llms, list_of_accurate_or_nonresponses, color='#e6007e')
    bars_nonanswers = ax.bar(['You'] + llms, list_of_accurate_responses, color='#12a19a')
    # Plot non-answers above the bars

    # Set the title and labels
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Compare Your Accuracy to the LLMs', fontsize=14, fontweight='bold')

    # Improve readability of x-axis labels
    plt.xticks(rotation=45, ha='right')

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

    # Customize the plot
    ax.set_facecolor('#f2f2f2')  # Set background color
    ax.grid(axis='y', linestyle='--', alpha=0.5)  # Add horizontal grid lines
    plt.xticks(fontsize=10)  # Adjust x-axis tick font size
    plt.yticks(fontsize=10)  # Adjust y-axis tick font size

    # Add a title and labels
    plt.title('Accuracy Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Models', fontsize=12)
    plt.ylabel('Number of correct responses', fontsize=12)

    # Add a legend
    ax.legend(['Did not answer', 'Accurate Answer'], loc='lower right', fontsize=10)

    # Adjust the layout
    plt.tight_layout()

    # Display the plot
    st.pyplot(fig)