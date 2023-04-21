import time

import streamlit as st
from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name,
    calc_md5,
    get_pages,
    _on_pages_changed
)


def hide_multi_pages():
    # https://discuss.streamlit.io/t/hide-show-pages-in-multipage-app-based-on-conditions/28642
    current_pages = get_pages(__file__)
    page_keys = [key for key, value in current_pages.items() if value['page_name'] != 'Home']
    for key in page_keys:
        del current_pages[key]


def load_multi_pages():
    pages = get_pages(__file__)
    main_script_path = Path(__file__)
    pages_dir = main_script_path.parent / "pages"
    script_paths = [f for f in pages_dir.glob("*.py") if f.name != '__init__.py']
    for path in script_paths:
        script_path_str = str(path.resolve())
        pi, pn = page_icon_and_name(path)
        psh = calc_md5(script_path_str)
        pages[psh] = {
            "page_script_hash": psh,
            "page_name": pn,
            "icon": pi,
            "script_path": script_path_str,
        }
        _on_pages_changed.send()


def check_password(form):
    """Returns `True` if the user had a correct password."""

    def validate():
        """Checks whether a password entered by the user is correct."""
        if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # First run, show inputs for username + password.
    # login_form = st.form(key='login')
    form.header('Login')
    form.text_input("Username", key="username")
    form.text_input(
        "Password", type="password", key="password"
    )
    form.form_submit_button("Submit", on_click=validate)
    if st.session_state.get("password_correct") is False:
        form.error("😕 User not known or password incorrect")
    elif st.session_state.get("password_correct") is True:
        login_tip = form.empty()
        for waiting_time in range(3, 0, -1):
            time.sleep(1)
            login_tip.success(f'login successfully! :) Auto redirecting after {waiting_time} seconds ...')
        st.session_state["authenticated"] = True
        return True
    else:
        st.session_state["authenticated"] = False
        return False


def show_welcome():
    st.header('😃 Greetings!')


if __name__ == '__main__':
    if st.session_state.get("authenticated") or not st.secrets.need_login:
        load_multi_pages()
        show_welcome()
    else:
        hide_multi_pages()
        login_form = st.empty()
        if check_password(login_form.form(key='login')):
            login_form.empty()
            st.balloons()
            load_multi_pages()
            show_welcome()
