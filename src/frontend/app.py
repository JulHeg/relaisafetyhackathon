import streamlit as st
import matplotlib.pyplot as plt
    
st.title('MindMatch: Comparing your Thinking Patterns to ChatGPT')

questions_answers = [
    {
        'question': 'Are you racist',
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
     }
]

correct_answers = 0
incorrect_answers = 0
# Keep track of the answered questions in the session state

if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = [False] * len(questions_answers)

for i, qa in enumerate(questions_answers):
    st.subheader(qa['question'])
    option = st.radio(
        "Choose your answer:",
        qa['answers'],
        key=f'question_{i}',
        disabled=st.session_state.answered_questions[i]
    )
    submitted = st.button('Submit', key=f'submit_{i}', disabled=st.session_state.answered_questions[i])
    if submitted:
        st.session_state.answered_questions[i] = True
        # Disable the button after submission
        correct_answer = qa['answers'][qa['correct_answer']]
        if option == correct_answer:
            st.write("Correct!")
            correct_answers += 1
        else:
            st.write(f"Incorrect answer: {correct_answer}")
            incorrect_answers += 1
        
        for model, model_answer in qa['llm_answers'].items():
            given_answer = qa['answers'][model_answer['answer']]
            confidence = model_answer['confidence']
            with st.expander(f"{model} answer: {given_answer} (Confidence: {confidence*100}%)", expanded=False):
                st.write(model_answer['explanation'])
                
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