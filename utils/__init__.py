from pathlib import Path

import pandas as pd
import streamlit as st


def load_prompt_templates():
    path = Path(__file__).parent.parent / "templates"
    return [f.name for f in path.glob("*.json")]


def load_prompts(template_name):
    if template_name:
        path = Path(__file__).parent.parent / "templates" / template_name
        return pd.read_json(path).drop_duplicates(subset='act').set_index('act')  # act, prompt


def render_footer():
    for _ in range(5):
        st.write('\n')
    st.markdown(
        "<br><hr><center>Made with ❤️ by ChatGPT and Streamlit. </center><hr>",
        unsafe_allow_html=True)
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)


def render_github_info(zone):
    with zone.container():
        for i in range(1):
            st.write("\n")
        st.markdown('<a href="https://github.com/haiichuan/chatgpt-streamlit" target="_blank" rel="chatgpt-streamlit">'
                    '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=chatgpt-streamlit" alt="GitHub">'
                    '</a>', unsafe_allow_html=True)
