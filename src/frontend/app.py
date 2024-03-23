import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import random
    
st.set_page_config(page_title='MindMatch', page_icon='🧪', layout="centered", initial_sidebar_state="expanded", menu_items=None)
st.title('MindMatch: Compare Your Thinking Patterns to ChatGPT')
st.sidebar.image('logo.jpg', width=300)
# Add a multiselect widget to allow the user to select multiple datasets
# The only possible values are 'CIFAR-10' and 'MNIST'

st.sidebar.markdown("# Compare your own performance to popular AI models")
datasets = st.sidebar.selectbox(
    'Select the datasets you want to try out:',
    ['Social-IQ'],
    index=0)
st.sidebar.write(
"""Welcome to MindMatch, a place where you can try out AI benchmarks and compare your results with those from popular large language models. This tool offers a simple way to get hands-on experience with AI, allowing you to see how these technologies perform compared to your own skills.

The app is straightforward, giving everyone, regardless of their expertise in AI, a chance to engage with and understand the capabilities of modern artificial intelligence. Through direct interaction, you can measure your answers against AI responses, providing insight into the current state of AI development.

It's an interesting opportunity to not only challenge the AI but also to challenge yourself, all while maintaining a modest level of enthusiasm. Whether you're curious about AI's abilities or just looking for a unique experience, this web app serves as a window into the advancements of artificial intelligence.

Done as part of the 2024 relAI Safety hackathon!"""
)
st.sidebar.image('relai.png', width=200)

# TODO: Replace these with real questions froma an LLM Benchmark
questions_answers = [
    {
        'question': 'Are you racist?',
        'answers': ['Yes', 'No', 'I am not sure'],
        'correct_answer': 1,
        'llm_answers': {
            'GPT-3': {
                'answer': 0,
                'confidence': 0.85,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            },
            'GPT-4': {
                'answer': 1,
                'confidence': 0.95,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            }
        }
        },
    {
        'question': 'Human dignity is',
        'answers': ['Unimpeachable', 'Delectable', 'Violable'],
        'correct_answer': 0,
        'llm_answers': {
            'GPT-3': {
                'answer': 1,
                'confidence': 0.85,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            },
            'GPT-4': {
                'answer': 2,
                'confidence': 0.95,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            }
        }
     },
    {
        'question': 'Human dignity is 2',
        'answers': ['Unimpeachable', 'Delectable', 'Violable'],
        'correct_answer': 0,
        'llm_answers': {
            'GPT-3': {
                'answer': 1,
                'confidence': 0.85,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            },
            'GPT-4': {
                'answer': 2,
                'confidence': 0.95,
                'explanation': 'The model has been trained on a diverse dataset and is not racist'
            }
        }
     }
]

random_subset_path = os.path.join('..', '..', 'data', 'random_subset.json')
with open(random_subset_path) as f:
    questions_subset = json.load(f)
questions_answers = []

for question in questions_subset[:3]:
    qa = {
        'question': question['context'] + ' ' + question['question'],
        'answers': [question['answerA'], question['answerB'], question['answerC']],
        'correct_answer': random.randint(0, 2),
        'llm_answers': {
            'GPT-3': {
                'answer': 1,
                'confidence': 0.85,
                'explanation': 'Answer elaboration A'
            },
            'GPT-4': {
                'answer': 2,
                'confidence': 0.95,
                'explanation': 'Answer elaboration B'
            }
        }
    }
    questions_answers.append(qa)

question_count = len(questions_answers)

# Keep track of the answered questions in the session state

if 'answers_given' not in st.session_state:
    st.session_state.answers_given = []

for i, qa in enumerate(questions_answers):
    # If one of the previous questions has not been answered, continue to the next question
    if i != len(st.session_state.answers_given):
        continue
        
    st.subheader(f'Question {i+1}/{question_count}: ' + qa['question'])
    option = st.radio(
        "Choose your answer:",
        qa['answers'],
        key=f'question_{i}',
        #disabled=st.session_state.answered_questions[i]
    )
    submitted = st.button('Check', key=f'submit_{i}', 
                          #disabled=st.session_state.answered_questions[i]
                          )
    correct_answer = qa['answers'][qa['correct_answer']]
    if submitted:
        # Disable the button after submission
        if option == correct_answer:
            st.write("Correct!")
        else:
            st.write(f"Incorrect answer: {correct_answer}")
        
        for model, model_answer in qa['llm_answers'].items():
            given_answer = qa['answers'][model_answer['answer']]
            confidence = model_answer['confidence']
            with st.expander(f"{model} answer: {given_answer} (Confidence: {confidence*100}%)", expanded=False):
                st.write(model_answer['explanation'])
        # Make a 'Next' button to go to the next question
    next = st.button('Next', key=f'next_{i}')
    print(next)
    if next:
        st.session_state.answers_given.append(option)
        # Update to remove the old question
        st.experimental_rerun()
            
                
# Once all questions are answered, show the final score
if len(st.session_state.answers_given) == len(questions_answers):
    
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