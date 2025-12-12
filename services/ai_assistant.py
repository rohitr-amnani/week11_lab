import streamlit as st
from openai import OpenAI

class AIAssistant:
    def __init__(self, api_key, system_role, session_key, role_name="AI"):
        self.client = OpenAI(api_key=api_key)
        self.system_role = system_role
        self.session_key = session_key
        self.role_name = role_name

        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = [
                {"role": "system", "content": self.system_role}
            ]

    def display_chat(self):
        st.divider()
        st.subheader("💬 AI Assistant")

        
        with st.sidebar:
            st.title("💬 Chat Controls")
            if st.button("🗑️ Clear Chat", key=f"clear_{self.session_key}", use_container_width=True):
                st.session_state[self.session_key] = [
                    {"role": "system", "content": self.system_role}
                ]
                st.rerun()

        
        for message in st.session_state[self.session_key]:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        
        user_input = st.chat_input(f"I am a {self.role_name} expert. How can I help you?")
        
        if user_input:
            
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state[self.session_key].append({"role": "user", "content": user_input})

            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                
                stream = self.client.chat.completions.create(
                    model="gpt-4.1-mini",  
                    messages=st.session_state[self.session_key],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            
            st.session_state[self.session_key].append({"role": "assistant", "content": full_response})