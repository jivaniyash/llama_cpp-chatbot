tool_get_weather = {
    "type":"function",
    "function":{
        "name":"get_weather",
        "description":"Get the current weather in a given location",
        "parameters":{
            "type":"object",
            "properties":{
                "location":{
                    "type":"string",
                    "description":"The city, e.g. San Francisco"
                },
                "unit":{
                    "type":"string",
                    "enum":[
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required":[
                "location",
                "unit"
            ]
        }
    }
}

# tool_get_Today = {
#     "type":"function",
#     "function":{
#         "name":"getToday",
#         "description":"Determine what day in calendar is today for converting user's relative date (like today, tomorrow, next week, next month etc.) into a full date format YYYY-MM-DD.",
#         "parameters":{
#             "type":"object",
#             "properties":{
#             },
#             "required":[
#             ]
#         }
#     }
# }