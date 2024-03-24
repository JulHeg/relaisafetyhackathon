import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import random
    
st.set_page_config(page_title='MindMatch', page_icon='🧪', layout="centered", menu_items=None, initial_sidebar_state='collapsed')
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(os.path.join('src', 'frontend', 'MindMatch-Logo_Horizontal.png'), width=350)
st.title('Compare Your Thinking Patterns to ChatGPT')
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 700px !important; # Set the width to your desired value
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
st.write(
"""Welcome to MindMatch, a place where you can try out AI benchmarks and compare your results with those from popular large language models. This tool offers a simple way to get hands-on experience with AI, allowing you to see how these technologies perform compared to your own skills.

The app is straightforward, giving everyone, regardless of their expertise in AI, a chance to engage with and understand the capabilities of modern artificial intelligence. Through direct interaction, you can measure your answers against AI responses, providing insight into the current state of AI development.

It's an interesting opportunity to not only challenge the AI but also to challenge yourself, all while maintaining a modest level of enthusiasm. Whether you're curious about AI's abilities or just looking for a unique experience, this web app serves as a window into the advancements of artificial intelligence.
""")
# Center this

with st.container(border=True):
    st.page_link("pages/SocialIQ.py", label="   Start Quiz", icon="🧪")

st.sidebar.write("Done as part of the 2024 relAI Safety hackathon!")
st.sidebar.image(os.path.join('src', 'frontend', 'relai.png'), width=200)
