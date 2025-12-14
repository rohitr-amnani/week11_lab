import streamlit as st
from openai import OpenAI

class AIAssistant:
    def __init__(self, system_role, session_key, role_name):
        # Directly initialize client using the secret
        self.client = OpenAI(api_key=st.secrets["openai_api_key"])
        
        self.system_role = system_role
        self.session_key = session_key
        self.role_name = role_name

        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = [
                {"role": "system", "content": self.system_role}
            ]

    def display_chat(self):
        # Display chat history
        for msg in st.session_state[self.session_key]:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # Chat Input
        if prompt := st.chat_input(f"I am  {self.role_name} Expert, how can i help you?"):
            # Add user message to state
            st.session_state[self.session_key].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Direct API call (No Try/Except)
                stream = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state[self.session_key],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                        
                message_placeholder.markdown(full_response)
                
                # Add assistant response to state
                st.session_state[self.session_key].append({"role": "assistant", "content": full_response})