import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import random
    
st.set_page_config(page_title='MindMatch', page_icon='🧪', layout="centered", menu_items=None)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(os.path.join('src', 'frontend', 'MindMatch-Logo_Horizontal.png'), width=350)
st.title('Compare Your Thinking Patterns to ChatGPT')
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important; # Set the width to your desired value
        }
        a[data-testid="stPageLink-NavLink"] {
            
            width: 100%;
        }
        .st-emotion-cache-8hkptd {
            margin-right: 1rem;
        }
        .st-emotion-cache-10fz3ls > p {
            font-size: 1.2rem;
            font-weight: 300;
        }
        a[data-testid="stPageLink-NavLink"] {
            align-items: center;
            justify-content: center;
        }
        div[data-testid="stSidebarUserContent"] {
            position: fixed;
            bottom: -50px;
        }
        .st-emotion-cache-vk3wp9 {
            background-color: rgb(255 255 255); 
            border-right: 0.75px solid;
            border-color: black;
        }
        .st-emotion-cache-1s3y5qe {
            color: black;
            border-bottom: 0.75px solid rgb(0 0 0 / 100%);
        }
        .st-emotion-cache-1oe5cao {
            min-height: 70vh;
        }
        .st-emotion-cache-nziaof {
            background-color: black;
            display: block;
        }
        .st-emotion-cache-nziaof:hover {
            background-color: white;
            border: 0.5px solid black;
            display:block
        }
        .st-emotion-cache-j7qwjs {
        }
        .st-emotion-cache-pkbazv {
            display: block;
            color: white;
        }
        .st-emotion-cache-pkbazv:active, .st-emotion-cache-pkbazv:visited, .st-emotion-cache-pkbazv:hover {
            display: block;
            color: black;
        }
        .st-emotion-cache-nziaof:active, .st-emotion-cache-nziaof:visited, .st-emotion-cache-nziaof:hover {
            text-decoration: none;
            font-weight: 600;
            color: black !important;
        }
        .st-emotion-cache-1r4qj8v {
            color: black;
        }
        h1 {
            color: black;
            font-family: Arial, sans-serif;
            font-weight: bold;
}
    </style>
    """,
    unsafe_allow_html=True,
)

# st.sidebar.image(os.path.join('src', 'frontend', 'logo.jpg'), width=300)
# Add a multiselect widget to allow the user to select multiple datasets
# The only possible values are 'CIFAR-10' and 'MNIST'

# st.sidebar.markdown("# Compare your own performance to popular AI models")
# datasets = st.sidebar.selectbox(
#     'Select the datasets you want to try out:',
#     ['Social-IQ'],
#     index=0)

st.write("""
[![Static Badge](https://img.shields.io/badge/VIEW%3A-GitHub_Repository-black?style=flat&logo=GitHub&logoColor=black&labelColor=white&link=https%3A%2F%2Fgithub.com%2FJulHeg%2Frelaisafetyhackathon)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FJulHeg%2Frelaisafetyhackathon)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FJulHeg%2Frelaisafetyhackathon&label=Visitors%3A&labelColor=%23000000&countColor=%23ffffff&style=flat&labelStyle=upper)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FJulHeg%2Frelaisafetyhackathon)
""")

# Introduction and description
st.markdown('''
Welcome to the AI & Human Quiz Challenge! This platform allows users to test their knowledge and reasoning skills against leading Language Models and AI systems. Whether you're curious about the latest in AI or just want to challenge yourself, you're in the right place.
''')


st.markdown("""
## How It Works
<ol>
    <li>Browse available quizzes from the sidebar.</li>
    <li>Select a quiz to see a brief explanation, including its scope and how to interpret your scores.</li>
    <li>Take the quiz and instantly see how you fared compared to both peers and AI.</li>
    <li>Navigate back to this page at any time to explore other quizzes.</li>
</ol>
""", unsafe_allow_html=True)

st.markdown('''
## Contributors
This project was made possible thanks to the dedication and hard work of our team (in alphabetical order):

- Gabriel Hamalwa
- Heather Dyett
- Hillary Hauger
- Jannes Elstner
- Julius Hege
- Richard Schwank

We appreciate the community's support and feedback to improve this platform. If you have any suggestions or wish to 
contribute, please visit our GitHub repository.

''')

st.sidebar.write("Done as part of the 2024 relAI Safety hackathon!")
st.sidebar.image(os.path.join('src', 'frontend', 'relai.png'), width=200)
