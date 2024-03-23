import streamlit as st
import requests
import matplotlib.pyplot as plt
import itertools
import urllib.parse

st.set_page_config(page_title='Manifold 2x2', page_icon='🔢', layout="centered", initial_sidebar_state="auto", menu_items=None)

default_markets = {
    "Starship orbital flight attempts occur in both November and December?": {
        "type": "binary",
        "A": "will-a-starship-orbital-flight-atte-887fb60c0e98" ,
        "B": "will-a-starship-orbital-flight-atte-890e74e896aa",
        "third":"will-starship-orbital-flight-attemp",
        "relation":"A and B"
    },
    "Israel-Hezbollah conflict killing >400 before 2023? And US and Iran at war before 2025?": {
        "type": "multi",
        "slug": "israelhezbollah-conflict-killing-40",
        "x": "Israel-Hezbollah conflict >400 deaths" ,
        "y": "US-Iran war"
    },
    "What will be the balance of power in Congress after the 2024 election?": {
        "type": "multi",
        "slug": "what-will-be-the-balance-of-power-i",
        "x": "Republican House" ,
        "y": "Republican Senate",
        "order": 6 #[(1,0), (1, 1), (0, 1), (0,0)]
    },
    "Will LK-99 replicate before 2025, and, will non-human UFO claims be confirmed by US gov by end of year?": {
        "type": "multi",
        "slug": "lk99-x-ufos-will-lk99-replicate-bef",
        "x": "LK-99" ,
        "y": "UFOs"
    },
    "Will Starship reach space in 2023? x Will a human land on the moon by 2028?": {
        "type": "multi",
        "slug": "will-starship-reach-space-in-2023-x",
        "x": "Starship reaches space in 2023",
        "y": "Human lands on the Moon by 2028"
    },
    "Bitcoin ETF (2023) x New all-time high (2024)?": {
        "type": "multi",
        "slug": "bitcoin-etf-2023-x-new-alltime-high",
        "x": "ETF" ,
        "y": "New ATH"
    },
    "Will Gemini be released before 2024? x Will GPT-5 be released before 2025?": {
        "type": "multi",
        "slug": "will-gemini-be-released-before-2024",
        "x": "Gemini released before 2024",
        "y": "GPT-5 released before 2025",
        "order": 4#[(1,1), (0, 1), (1, 0), (0,0)]
    },
    "Will the 2025 US federal deficit be >$1.7T, and which party will win the 2024 Presidential election?": {
        "type": "multi",
        "slug": "will-the-2025-us-federal-deficit-be",
        "x": ">$1.7T deficit" ,
        "y": "Democrat wins presidency"
    },
    "Conditional on Aella getting new cavities, will 10000+ people get Lantern Bioworks' cavity prevention treatment?": {
        "type": "multi",
        "slug": "conditional-on-aella-getting-new-ca",
        "x": "Aella gets new cavities" ,
        "y": ">= 10000 people get treatment"
    },
    "Russia coup-nuke combination market": {
        "type": "multi",
        "slug": "russia-coupnuke-combination-market",
        "x": "Coup or regime change before December 31, 2024?" ,
        "y": "Will Russia nuke Ukraine?"
    }
}

params = st.experimental_get_query_params()
is_embed = params.get('embedded', ['false'])[0] == 'true'

default_type = params.get('type', ['multi'])[0]
market_type_labels = {
    'Binary': 'binary',
    'Multiple choice': 'multi',
}
if default_type in market_type_labels.keys():
    default_type_index = list(market_type_labels.values()).index(default_type)
if not is_embed:
    st.title('Manifold 2x2 Viewer')
else:
    st.markdown("""<style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        img {
            width: auto !important; 
            max-width: 80vw;
            max-height: 90vh;
        }
        button[title="View fullscreen"]{
            visibility: hidden;
        }
        header {
            visibility: hidden;
        }
    </style>
    """, 
    unsafe_allow_html=True)
def encode_params(save_params):
    url = '/?'
    save_url = url + urllib.parse.urlencode(save_params)
    return save_url

def explainer_text():
    with st.expander("What is this?"):
        st.write("""On [Manifold Markets](https://manifold.markets), people can bet on whether or not things will happen. With a bit of trying they can even bet on the combination of two events. This tool draws a [mosaic plot](https://en.wikipedia.org/wiki/Mosaic_plot) to visualize the probabilities and correlation between two binary events.

The mosaic plot is a graphical representation of the joint and conditional probabilities. The overall square has area 1 and represents the total probability space. The 2x2=4 colored squares represent the possible combinations of two events happening or not, their areas are their likelihoods. The lower left square is the probability that both events happen, the upper right that neither happens. You can read off the marginal probability of the first event (that on the x-axis) by the width of the lower left rectangle. The heights of the two lower rectangles are the probabilities of the second event (that on the y-axis) conditional on the first happening or not.

There are two ways to ask about two event at once on Manifold: The first to ask a multiple choice question featuring all four combinations of the two events. The second is two ask about two events individually as binary markets and then also ask a third question about the relationship between the two events. You can input both here.

Here are some examples:""")
        question_text = []
        for market in default_markets.keys():
            save_url = encode_params(default_markets[market])
            question_text.append(f"- [{market}]({save_url})")
        st.write('\n'.join(question_text))
    
if is_embed:
    market_type = default_type
else:
    explainer_text()
    market_type_str = st.selectbox('Choose market type', market_type_labels.keys(), index=default_type_index)
    market_type = market_type_labels[market_type_str]

def expand_yesno(title):
    if len(title) == 0:
        return "Yes/No"
    else:
        return title + " (Yes/No)"

if default_type == "custom1":
    req = requests.get('https://manifold.markets/api/v0/slug/will-republicans-win-pennsylvania-g')
    if req.status_code != 200:
        st.write(f'Could not load market')
        st.stop()
    json = req.json()
    answers = json['answers']
    bools_to_prob = {
        (1,1): answers[2]['probability'],
        (1,0): answers[3]['probability'],
        (0,1): answers[4]['probability'],
        (0,0): answers[5]['probability'],
    }
    # Normalize so that the sum of the probabilities is 1
    total = sum(bools_to_prob.values())
    bools_to_prob = {k: v/total for k, v in bools_to_prob.items()}
    x_label = "Republicans win Pennsylvania"
    y_label = "Republicans win Georgia"
    
elif market_type == "multi":
    default_slug = params.get('slug', [''])[0]
    default_x = params.get('x', [''])[0]
    default_y = params.get('y', [''])[0]
    default_order_index = int(params.get('order', ["0"])[0])
    if is_embed:
        slug = default_slug
    else:
        slug = st.text_input('Enter slug', value=default_slug)
    slug = slug.split('/')[-1]
    if len(slug) == 0:
        st.stop()
    if is_embed:
        x_label = default_x
        y_label = default_y
    else:
        x_label = st.text_input('First condition label', value=default_x)
        y_label = st.text_input('Second condition label', value=default_y)
    default_order = [(1,1), (1,0), (0,1), (0,0)] 
    # Get all permutations of default_order
    permutations = list(itertools.permutations(default_order))
    orderings = {}
    for permutation in permutations:
        pretty_string = ', '.join([f'{["No", "Yes"][x[0]]}/{["No", "Yes"][x[1]]}' for x in permutation])
        orderings[pretty_string] = permutation
    if is_embed:
        order_string = list(orderings.keys())[default_order_index]
    else:
        order_string = st.selectbox('What order do the answers appear in?', list(orderings.keys()), index=default_order_index)
    order_index = list(orderings.keys()).index(order_string)
    order = orderings[order_string]
    
    req = requests.get('https://manifold.markets/api/v0/slug/' + slug)
    if req.status_code != 200:
        st.write(f'Could not load market with slug {slug}')
        st.stop()
    json = req.json()
    if json['mechanism'] != 'cpmm-multi-1':
        st.write(f'Market selected is not multiple-choice')
        st.stop()
    if len(json['answers']) != 4:
        st.write(f'Market selected does not have 4 answers')
        st.stop()
    bools_to_prob = {}
    i_to_bools = order

    for i, answer in enumerate(json['answers']):
        bools = i_to_bools[i]
        bools_to_prob[tuple(bools)] = answer['probability']
else: # binary markets+
    default_market_A_slug = params.get('A', [''])[0]
    default_market_B_slug = params.get('B', [''])[0]
    default_market_third_slug = params.get('third', [''])[0]
    default_relation = params.get('relation', ['A and B'])[0]
    relations = ["A and B", "A or B", "A xor B", "A given B", "B given A"]
    if is_embed:
        market_A_slug = default_market_A_slug
        market_B_slug = default_market_B_slug
        market_third_slug = default_market_third_slug
        relation = default_relation
    else:
        market_A_slug = st.text_input('Market A slug or URL', value=default_market_A_slug)
        market_A_slug = market_A_slug.split('/')[-1]
        market_B_slug = st.text_input('Market B slug or URL', value=default_market_B_slug)
        market_B_slug = market_B_slug.split('/')[-1]
        market_third_slug = st.text_input('Third market slug or URL', value=default_market_third_slug)
        market_third_slug = market_third_slug.split('/')[-1]
        default_relation_index = relations.index(default_relation)
        relation = st.selectbox('What does the third market represent?', relations, index=default_relation_index)
    if len(market_A_slug) == 0:
        st.stop()
    if len(market_B_slug) == 0:
        st.stop()
    if len(market_third_slug) == 0:
        st.stop()
    slugs = [market_A_slug, market_B_slug, market_third_slug]
    probabilities = []
    for i, slug in enumerate(slugs):
        req = requests.get('https://manifold.markets/api/v0/slug/' + slug)
        if req.status_code != 200:
            st.write(f'Could not load market with slug {slug}')
            st.stop()
        json = req.json()
        if json['mechanism'] != 'cpmm-1':
            st.write(f'Market {slug} is not binary')
            st.stop()
        probabilities.append(json['probability'])
        if i == 0:
            x_label = json['question']
        elif i == 1:
            y_label = json['question']
    
    if relation == "A and B":
        both_prob = probabilities[2]
    elif relation == "A or B":
        both_prob = probabilities[0] + probabilities[1] - probabilities[2]
    elif relation == "A xor B":
        both_prob = (probabilities[0] + probabilities[1] - probabilities[2])/2
    elif relation == "A given B":
        both_prob = probabilities[2] * probabilities[1]
    elif relation == "B given A":
        both_prob = probabilities[2] * probabilities[0]
    else:
        st.write(f"Unknown relation {relation}")
        st.stop()
        
    bools_to_prob = {
        (1,1): both_prob,
        (1,0): probabilities[0] - both_prob,
        (0,1): probabilities[1] - both_prob,
        (0,0): 1 - probabilities[0] - probabilities[1] + both_prob,
    }
    
    if min(bools_to_prob.values()) < 0:
        st.warning('Given set of markets is not consistent', icon="⚠️")
    
assert abs(sum(bools_to_prob.values()) - 1) < 0.0001

default_swap_axes = params.get('swap', ['false'])[0] == 'true'
if is_embed:
    swap_axes = default_swap_axes
else:
    swap_axes = st.checkbox('Swap axes', value=default_swap_axes)
if swap_axes:
    bools_to_prob = {(y,x): bools_to_prob[(x,y)] for (x,y) in bools_to_prob.keys()}
    y_label, x_label = x_label, y_label

# Initialize the figure and axis
if is_embed:
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
else:
    fig, ax = plt.subplots(figsize=(6, 6))

# Define colors for each rectangle
colors = ['red', 'green', 'blue', 'purple']

# Plot rectangles for A
B_given_A = bools_to_prob[(1,1)] / (bools_to_prob[(1,0)]+bools_to_prob[(1,1)])
ax.add_patch(plt.Rectangle((0, 0), bools_to_prob[(1,0)]+bools_to_prob[(1,1)], B_given_A, color=colors[0], alpha=0.6))
ax.add_patch(plt.Rectangle((0, B_given_A), bools_to_prob[(1,0)]+bools_to_prob[(1,1)], 1-B_given_A, color=colors[1], alpha=0.6))

# # Plot rectangles for not A
B_given_not_A = bools_to_prob[(0,1)] / (bools_to_prob[(0,0)]+bools_to_prob[(0,1)])
ax.add_patch(plt.Rectangle((bools_to_prob[(1,0)]+bools_to_prob[(1,1)], 0), bools_to_prob[(0,0)]+bools_to_prob[(0,1)], B_given_not_A, color=colors[2], alpha=0.6))
ax.add_patch(plt.Rectangle((bools_to_prob[(1,0)]+bools_to_prob[(1,1)], B_given_not_A), bools_to_prob[(0,0)]+bools_to_prob[(0,1)], 1-B_given_not_A, color=colors[3], alpha=0.6))

P_A = bools_to_prob[(1, 1)] + bools_to_prob[(1, 0)]
P_B = bools_to_prob[(1, 1)] + bools_to_prob[(0, 1)]

#  correlation coefficient
r = (bools_to_prob[(1, 1)] - (P_A * P_B)) / (P_A * (1 - P_A) * P_B * (1 - P_B))**0.5

# Set limits and labels
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# x_label_yesno = expand_yesno(x_label)
# y_label_yesno = expand_yesno(y_label)
# ax.set_xlabel(x_label_yesno)
# ax.set_ylabel(y_label_yesno)
if len(x_label) > 0:
    ax.set_xlabel(x_label)
if len(y_label) > 0:
    ax.set_ylabel(y_label)


plt.text(P_A + 0.01, 0.02, f'{P_A:.0%}')#
plt.text(P_A  / 2, bools_to_prob[(1, 1)] / P_A + 0.01, f'{bools_to_prob[(1, 1)] / P_A:.0%}', ha ='center')
plt.text(P_A + (1-P_A)  / 2, bools_to_prob[(0, 1)] / (1-P_A) + 0.01, f'{bools_to_prob[(0, 1)] / (1-P_A):.0%}', ha ='center')
plt.text(P_A  / 2, 0.02, "Yes", ha ='center')
plt.text(P_A + (1-P_A)  / 2, 0.02, "No", ha ='center')
plt.text(0.01, bools_to_prob[(1, 1)] / P_A / 2, "Yes")
plt.text(0.01, bools_to_prob[(1, 1)] / P_A  + bools_to_prob[(1, 0)] / P_A / 2, "No")

st.pyplot(fig)
st.write(f"""The correlation coefficient is {r:.2f}.""")
if market_type == "multi" or market_type == "binary":
    # Show a link from embed to editably or vice versa
    if market_type == "multi":
        save_params = {
            'type': 'multi',
            'slug': slug,
            'x': x_label,
            'y': y_label,
            'swap': 'true' if swap_axes else 'false',
            'order': order_index,
        }
    else:
        save_params = {
            'type': 'binary',
            'A': market_A_slug,
            'B': market_B_slug,
            'third': market_third_slug,
            'swap': 'true' if swap_axes else 'false',
            'relation': relation,
        }
    if is_embed:
        explainer_text()
        save_url = encode_params(save_params)
        st.markdown(f"[Edit using this link]({save_url})")
    else:
        save_params["embedded"] = "true"
        save_url = encode_params(save_params)
        st.markdown(f"[Share using this link]({save_url})")
    
# Examples: 
# http://localhost:8501/?type=multi&slug=lk99-x-ufos-will-lk99-replicate-bef&x=&y=&order=0
# http://localhost:8501/?type=binary&A=will-a-starship-orbital-flight-atte-887fb60c0e98&B=will-a-starship-orbital-flight-atte-890e74e896aa&third=will-starship-orbital-flight-attemp&relation=A+and+B
# http://localhost:8501/?type=multi&slug=starship-launch-attempt-in-november&x=Starship+launch+attempt+in+November&y=Starship+launch+attempt+in+December&order=4
# http://localhost:8501/?type=binary&A=will-a-starship-orbital-flight-atte-887fb60c0e98&B=will-a-starship-orbital-flight-atte-890e74e896aa&third=will-starship-orbital-flight-attemp&relation=A+and+B
