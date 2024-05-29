import logging 
from llama_cpp import Llama
import os
import subprocess

logging.info("Running llm.py file")
def download_model(model_name):
    model_directory = "./models "

    # check if model directory exists
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
        logging.info(f"Directory has been created -> {model_directory}")
    
    # download model
    download_links = {"functionary-small-v2.2.q4_0.gguf":"https://huggingface.co/meetkai/functionary-small-v2.2-GGUF/resolve/main/functionary-small-v2.2.q4_0.gguf",
                        "llama-2-7b.Q2_K.gguf":"https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q2_K.gguf",
                        "Phi-3-mini-4k-instruct-q4.gguf":"https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"}
    
    download_link = download_links[model_name]
    try:
        # Run the command using subprocess and capture the output
        result = subprocess.run(
            ["wget", download_link, "-P", model_directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # Log the output
        logging.info(result.stdout)
        if result.returncode == 0:
            logging.info(f"Successfully downloaded model & saved to {model_directory}...")
        else:
            logging.error(f"Failed to download model. Return code: {result.returncode}")
            logging.info(result.stdout)
            logging.error(result.stderr)
    except Exception as e:
        logging.exception(f"Exception occurred: {e}")

def load_model(model_name):
    model_path = f"./models/{model_name}"

    # if model-card doesn't exist
    if not os.path.exists(model_path): 
        llm = download_model(model_name)
        
    # Create Llama Instance    
    try:
        logging.info(f"Loading {model_name} in RAM")
        llm = Llama(
            model_path=model_path,
            chat_format="chatml-function-calling",
            max_tokens=5000,
            n_ctx=5000
            # use_mlock=True
        )
        logging.info(f"Successfully loaded {model_name} in RAM")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        llm = None
    
    return llm

