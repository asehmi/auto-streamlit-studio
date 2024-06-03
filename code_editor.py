from streamlit_ace import st_ace
import streamlit as st
import os
import time
from utils import check_syntax


def display_code_editor():
    if (
        "temp_file_path" in st.session_state
        and st.session_state.temp_file_path
        and os.path.exists(st.session_state.temp_file_path)
    ):
        with open(st.session_state.temp_file_path, "r") as file:
            initial_code = file.read()
    else:
        initial_code = "# Your code will appear here."

    # Display the Ace Editor
    with st.sidebar:
        edited_code = st_ace(
            value=initial_code, language="python", theme="monokai", key="ace_editor"
        )

        # Button to save the edited code
        if st.button("Save Code"):
            valid, error_message = check_syntax(edited_code)

            if valid:
                with open(st.session_state.temp_file_path, "w") as file:
                    file.write(edited_code)
                st.session_state.temp_file_content = edited_code
                # Add edited code as it was produced by assistant
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"```\n{edited_code}\n```"}
                )
                st.success("Code saved successfully!")
                time.sleep(1)  # Add a delay of 2 seconds
                st.rerun()
            else:
                st.error(f"Syntax error in code: {error_message}")