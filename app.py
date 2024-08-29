import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import os
from openai import OpenAI

client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

def on_input_change():
    prompt = st.session_state.user_input
    response = client.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=[{'role': 'user', 'content': prompt}]
    )

    prompt_response = response.choices[0].message.content

    st.session_state.past.append(prompt)
    st.session_state.generated.append({'type': 'normal', 'data': prompt_response})
    st.session_state.user_input = ""

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

st.session_state.setdefault(
    'past', 
    []
)

st.session_state.setdefault(
    'generated', 
    []
)

st.title("AI-PAPER-BOT")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")