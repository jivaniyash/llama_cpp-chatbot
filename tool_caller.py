from tools import tool_get_weather
from functions import get_weather
import json
import logging

# Define a mapping from function names to function implementations
function_mapping = {
    "get_weather": get_weather,
    # "getToday": getToday,
}

def tool_retreiver(tool_calls: list):
    logging.info(f"Running tool_retreiver: {tool_calls}")
    tool_call = tool_calls[0]
    assert tool_call['type'] == 'function'

    function_name = tool_call['function']['name']
    function_params = json.loads(tool_call['function']['arguments'])

    function_response = function_mapping[function_name](**function_params)
    logging.info(f"response from function: {function_response}")

    # tool_message = {'role': "assistant", "content": function_response}
    # tool_message = {"role":"tool", "content":function_response} 
    
    # tool_message = {"tool_call_id": tool_call['id'], "role":"tool", "name": function_name, "content":function_response} 

    # tool_message = {"role":"tool", "name":function_name, "content":function_response}

#     tool_message = {
#     "role": "assistant",
#     "tool_calls": [json.dumps({"id": tool_call['id'], "function": function_response, "type": "function"})]
# }
    return function_response