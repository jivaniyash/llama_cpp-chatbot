import json
from typing import Literal

def get_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""

    import random
    # default weather info - can be changed to hit database/3-rd party APIs to get real-time weather info
    # Workflow Steps
    # <!-- - Fetch latitude and longitudes from [dataset](https://simplemaps.com/data/world-cities)  future scope--> 
    # connect to sql database 

    weather_info = {"location": location, 
            "temperature": random.choice(range(50,90,1)), 
            "unit": unit, 
            "precipitation": "low"}

    return f"The temperature at {location} is {weather_info['temperature']} fahrenheit with {weather_info['precipitation']} precipitation."


# def getToday():
#     """
#     Determine today's date.

#     Args:
#         None
#     """
#     import datetime
#     date = datetime.date.today()
#     date_info = {"date": date.strftime("%Y-%m-%d"),
#                        "format": "%Y-%m-%d"}

#     return f"Todays date is {date_info['date']} in {date_info['format']} format."