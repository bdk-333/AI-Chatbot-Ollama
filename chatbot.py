import streamlit as st
import requests
import time
import json

# app config
st.set_page_config(
    page_title="Ollama Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

URL = "http://localhost:11434/api/chat"

AVAILABLE_MODELS = (
    "llama3.2:latest",
    "qwen3:4b-q4_K_M"
)

def initialize_session_state():
    
    # default model is at index 0
    if "current_model" not in st.session_state:
        st.session_state.current_model = AVAILABLE_MODELS[0]
        
    # create different history for each model
    for model in AVAILABLE_MODELS:
        if f"messages_{model}" not in st.session_state:
            st.session_state[f"messages_{model}"] = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                }
            ]


def get_current_chat_history():
    return st.session_state[f"messages_{st.session_state.current_model}"]


def get_streamed_response(prompt):
    messages = get_current_chat_history()
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    
    json_data = {
        "model": st.session_state.current_model,
        "messages": messages,
        "stream": True
    }
    
    in_think_block = False
    buffer = ""
    
    try:
        response = requests.post(url=URL, json=json_data, stream=True)
        response.raise_for_status()
        
        # full_response = ""
        
        # iterate over the response stream line by line
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line)
                    if "message" in json_line and "content" in json_line['message']:
                        token = json_line['message']['content']
                        buffer += token
                        
                        # process buffer text for think tags
                        while True:
                            if not in_think_block:
                                start_idx = buffer.find("<think>")
                                
                                if start_idx != -1:
                                    # from the first letter to the start of think tag as answer
                                    if start_idx > 0:
                                        yield "answer", buffer[:start_idx]
                                    buffer = buffer[start_idx + len("<think>"):]
                                    in_think_block = True   # Now, are inside the think block
                                else:
                                    # think tag is not found, the entire buffer text is answer
                                    yield "answer", buffer
                                    buffer = ""   # emptying buffer for next iteration
                                    break   # breaking out of processing buffer loop, as we didnt find any think tag
                            else:
                                end_index = buffer.find("</think>")
                                if end_index != -1:
                                    if end_index > 0:
                                        yield "think", buffer[:end_index]
                                    buffer = buffer[end_index + len("</think>"):]
                                    in_think_block = False
                                else:
                                    yield "think", buffer
                                    buffer = ""
                                    break
                                
                except Exception as e:
                    print(e)
                    break
        
    except Exception as e:
        print(e)
        
        
# App UI
st.title("Ollama-powered ChatBot")
st.caption("A local chatbot powered by Ollama running locally...")

# model selection from the sidebar
with st.sidebar:
    st.header("Model Selection: ")
    st.write("Select one of the following model.")
    st.caption("Note that changing model will reset the session")
    
    selected_model = st.selectbox(
        "Select: ",
        AVAILABLE_MODELS,
        key="current_model"
    )


# initializing session
initialize_session_state()

# display chat messages from the history, if any
for message in get_current_chat_history():
    
    # skipping system role and displaying other messages
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# main chat input
if prompt := st.chat_input("What would you like to ask?"):    # get prompt from the user
    
    # user prompts
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # model outputs
    with st.chat_message("assistant"):
        
        # creating empty thinking and actual response container
        think_expander = st.expander("Show though process...", expanded=False)
        think_container = think_expander.empty()
        answer_container = st.empty()
        
        # thinking and answer content to display
        think_content = ""
        answer_content = ""
        
        # for each token, check part type and assign it to respective content
        for part_type, token in get_streamed_response(prompt):
            if part_type == "think":
                think_content += token
                think_container.info(think_content)
            else:
                answer_content += token
                answer_container.markdown(answer_content)
    
    get_current_chat_history().append({"role": "assistant", "content": answer_content})