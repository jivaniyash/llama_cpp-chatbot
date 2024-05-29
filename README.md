## LLM Chat Assistant using LLAMA CPP

#### STREAMLIT INTERFACE

![](https://github.com/jivaniyash/llama_cpp-chatbot/blob/main/gif/chat_interface.gif)

## 
Steps to work on the ChatBot
- This project is developed in GCP VM instance. Follow the steps from [connect_vm_ssh.md](https://github.com/jivaniyash/llama_cpp-chatbot/blob/main/connect_vm_ssh.md) to connect local VS code using SSH tunneling.

- Clone this repo - `git clone https://github.com/jivaniyash/llama_cpp-chatbot.git`

1. Create Virtual Env inside VM
    ```bash
    sudo apt update
    sudo apt install virtualenv

    cd ./project
    virtualenv <env_name>

    source <env_name>/bin/activate # to activate environment
    ```

2. Install Dependencies
    ```bash
    pip install -r requirements.txt -q
    ```

3. Run `streamlit run ./app.py`. It will start a UI interface running on default port `3501`

---
### Project Description
- There are 3 LLMs explored which can be used in devices running on CPUs

    1. [functionary-small-v2.2.q4_0.gguf](https://huggingface.co/meetkai/functionary-small-v2.2-GGUF/resolve/main/functionary-small-v2.2.q4_0.gguf)

  2. [llama-2-7b.Q2_K.gguf](https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q2_K.gguf)

  3. [Phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

- Logs are recorded in `./logs/logs-<date-time>.log` file to debug the application.
- `tools.py` contains functions accepted by the LLM format
- UI interface 
    - Select Model from Left Side Panel
    - Click on `CLear Message` Button to clear the history & load model
    - Put a checkbox on `Use Tools` if you want LLM to call functions to call the tool. (Currently, only sample function is added to check the working of the model)
    - LLM generates a response with `stream=True` which is used for front-end applications to send the assistant prompt to the user as soon as the response is ready to deliver. 

