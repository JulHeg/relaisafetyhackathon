import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import random
    
st.title('MindMatch: Comparing your Thinking Patterns to ChatGPT')

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

correct_answers = 0
incorrect_answers = 0
# Keep track of the answered questions in the session state

if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = [False] * len(questions_answers)

for i, qa in enumerate(questions_answers):
    # If one of the previous questions has not been answered, continue to the next question
    if i > 0 and not st.session_state.answered_questions[i-1]:
        break
    if st.session_state.answered_questions[i]:
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
    if option == correct_answer:
        correct_answers += 1
    else:
        incorrect_answers += 1
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
        print('test')
        st.session_state.answered_questions[i] = True
        # Update to remove the old question
        st.experimental_rerun()
            
                
# Once all questions are answered, show the final score
if all(st.session_state.answered_questions):
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
    fig, ax = plt.subplots()
    ax.bar(llms_accuracy.keys(), llms_accuracy.values())
    ax.set_ylabel('Accuracy')
    ax.set_title('Compare your accuracy to the LLMs')
    # y limits
    ax.set_ylim(0, 1)

    

    st.pyplot(fig)