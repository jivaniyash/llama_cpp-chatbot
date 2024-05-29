import streamlit as st
import logging
import log_config  # Ensure this sets up logging
from llm_model import load_model
import json
from tool_caller import tool_retreiver
from tools import tool_get_weather


# App title
st.set_page_config(page_title="💬 LLM Chatbot")
# Streamlit app interface
st.title("LLM Streamlit App")
with st.sidebar:
    st.title("💬 MY Custom LLM Chatbot")
    st.write('This chatbot is created using the open-source LLM functionary model.')
    st.markdown('Create your custom bot using the [link](https://github.com/jivaniyash/llama_cpp-chatbot/tree/main)')

    st.subheader('Models')
    selected_model = st.sidebar.selectbox('Choose a model', ['functionary-small-v2.2.q4_0.gguf', 'llama-2-7b.Q2_K.gguf', 'Phi-3-mini-4k-instruct-q4.gguf'], key='selected_model')
    # User input section with checkbox
    use_tools = st.checkbox('Use tools', key='use_tools_checkbox')

# Ensure the LLM object is available
with st.spinner("Loading Model ..."):
    llm = load_model(selected_model)
    if llm is None:
        st.error("Failed to load the model. Please check the logs for more details.")
        logging.error("Failed to load the model. llm_object is None.")
        st.stop()

# Store LLM generated responses
greeting_message = "How may I assist you today?"
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "system", "content": "A chat between a user and an AI assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. The assistant calls functions with appropriate input when necessary."},
        {"role": "assistant", "content": greeting_message}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    # clear ram
    global llm
    try:   
        del llm
        logging.info("llm_ object is cleared from memory")
    except Exception as e:
        logging.info(f"Error deleting llm: {e}")
        
    st.session_state.messages = [
        {"role": "system", "content": "A chat between a user and an AI assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. The assistant calls functions with appropriate input when necessary."},
        {"role": "assistant", "content": greeting_message}
    ]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function to get response from LLM
def generate_response(messages, use_tools=True):
    logging.info(f"Generating response from LLM: {messages}")
    try:
        if use_tools: 
            logging.info("using tool_calls to chat completion")
            response = llm.create_chat_completion(
                messages=messages,
                tools=[tool_get_weather],
                tool_choice='auto',
            )
            logging.info(f"Received response from LLM {response}")

            # check if assistant is referring to tool_call
            if 'tool_calls' in response['choices'][0]['message']:
                # st.session_state.messages.append(response_message) 

                logging.info("Retreiving from tool")
                tool_message = tool_retreiver(response['choices'][0]['message']['tool_calls'])
                logging.info(f"Received response from tool {tool_message}")
                return tool_message
        else:
            response = llm.create_chat_completion(
                messages=messages,
                stream=True
            )
            logging.info(f"Received response from LLM {response}")
            return response
            # return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error getting response from LLM: {e}")
        st.error("An error occurred while getting response from the model. Please check the logs.")
        return None


# User-provided prompt
if prompt := st.chat_input(placeholder="Type your message here and press Enter.", disabled=False):
    # User input section with checkbox
    # use_tools = st.checkbox('Use tools')
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner('Getting response from the model...'):
            assistant_response = generate_response(st.session_state.messages, use_tools=use_tools)

            if use_tools:
                placeholder = st.empty()
                placeholder.markdown(assistant_response)
                assistant_message = {"role": "assistant", "content": assistant_response}
                st.session_state.messages.append(assistant_message)
            else:
                placeholder = st.empty()
                full_response = ''
                for word in assistant_response:
                    # if isinstance(item, dict):
                    #     item = json.dumps(item)
                    if 'content' in word['choices'][0]['delta']:
                        item = word['choices'][0]['delta']['content']
                        # print(item)
                        full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
                logging.info(f"Generator object LLM repsonse: {full_response}")
                assistant_message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(assistant_message)