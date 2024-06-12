from py2gpt import create_openai_function_description
from typing import Literal

def get_current_weather(location: str, format: Literal["fahrenheit", "celsius"] = "fahreneit"):
    """
    Get the current weather.

    Args:
        location: Name of the city , e.g., San Francisco.
        format: The temperature unit to use.
    """
    location = location + " __ "
    return f"Weather for {location} is 20 degrees {format}"

# Pass the function definition node and the function object to the function
json_o = create_openai_function_description(get_current_weather)
print(json_o)
