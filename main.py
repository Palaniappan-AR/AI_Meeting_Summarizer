import openai
import json

openai.api_key = "your-api-key"

# Define available functions with diverse examples
def extract_action_items(args):
    return f"Extracted action items: {args['action_items']}"

def classify_meeting_type(args):
    return f"Meeting type classified as: {args['meeting_type']}"

def analyze_meeting_sentiment(args):
    return f"Sentiment analysis result: {args['sentiment']}"

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function mapping
available_functions = {
    "extract_action_items": extract_action_items,
    "classify_meeting_type": classify_meeting_type,
    "analyze_meeting_sentiment": analyze_meeting_sentiment
}

# Functions metadata with 'required' fields
functions = [
    {
        "name": "extract_action_items",
        "description": "Extracts action items from a meeting transcript.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "A brief meeting summary."},
                "action_items": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of action items discussed."
                }
            },
            "required": ["summary", "action_items"]
        }
    },
    {
        "name": "classify_meeting_type",
        "description": "Classifies the type of meeting.",
        "parameters": {
            "type": "object",
            "properties": {
                "meeting_type": {
                    "type": "string",
                    "enum": ["Stand-up", "Planning", "Retrospective", "General"],
                    "description": "Type of the meeting."
                }
            },
            "required": ["meeting_type"]
        }
    },
    {
        "name": "analyze_meeting_sentiment",
        "description": "Analyzes the overall sentiment of the meeting.",
        "parameters": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["Positive", "Neutral", "Negative"],
                    "description": "Sentiment of the meeting."
                }
            },
            "required": ["sentiment"]
        }
    }
]

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

# Chat Completion and function handling
def summarize_meeting(transcript):
    messages=[
            {"role": "system", "content": "You are a helpful assistant for summarizing meetings, extracting action items, and analyzing meeting details."},
            {"role": "user", "content": f"Process this meeting transcript: {transcript}"},
        ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)

        if not function_to_call:
            return "Error: Function not found."

        # Parse function arguments and execute the function
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(function_args)

        # Append the function response to messages
        messages.append(response_message)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": str(function_response)
        })

        # Get a new response with the function call's result in context
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return second_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]


transcript = """
John: We need to improve the website’s loading speed.
Sarah: I'll handle the SEO updates. The delay in loading time is frustrating.
Mark: I'll work on reducing image sizes and optimizing code.
"""

response = summarize_meeting(transcript)
print(response)

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

# First Response:
# {
#   "function_call": {
#     "name": "extract_action_items",
#     "arguments": "{\"summary\": \"Discussion on improving website loading speed.\", \"action_items\": [\"Sarah to handle SEO updates\", \"Mark to reduce image sizes and optimize code\"]}"
#   }
# }

# function_to_call --> available_functions
# Extracted action items: ['Sarah to handle SEO updates', 'Mark to reduce image sizes and optimize code']

# Second Response:
# Action items have been identified: 
# Sarah will handle SEO updates.
# Mark will work on reducing image sizes and optimizing code.
