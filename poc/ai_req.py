import requests
from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()

# OpenAI API Configuration
API_URL = "https://api.pawan.krd/v1/chat/completions"
API_KEY = os.getenv("OPEN_API_KEY")  # Replace with your OpenAI API key

# Function to send the prompt to the AI

# openai.api_key = API_KEY


def write_to_file(data):
    with open("./poc/responses/response3.txt", "w") as file:
        file.write(data)

# User Input
def gen_response(location, activity_type, budget, number_of_locations, group, duration, activity_level):
    initial_msg = f"""Based on the input generate an activity recommendation in JSON format:
    {{
        "name_of_location": "string",
        "description": "string",
        "budget_breakdown": "string",
        "wellbeing_impact": "string"
    }}
    In the "wellbeing_impact" field you have to talk about how it possitively affects the individual's mental and physical health.
    In the "name_of_location" field you have to talk about the specific name of the location.
    The budget breakdown should be contain the cost of the activity. Make sure to take into account the user's total budget
    """
    
    prompt = f"""
    Can you recommend a journey (multiple activities) in {location} consisting of {number_of_locations} different locations based on the following factors:
    - Type: {activity_type}
    - Budget: {budget}
    - Group size: {group}
    - Duration: {duration}
    - Level of physical activity: {activity_level}
    """
    
    client = openai.OpenAI()
    # client.api_key = API_KEY
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" for higher-quality responses
        messages=[
            {"role": "system", "content": initial_msg},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    
    print(response.choices[0].message.content)
    try:
        result_json = json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        result_json = {"error": "Invalid JSON format returned by AI."}
    
    return result_json

def get_user_input():
    location = "Cluj-Napoca"
    activity_type = "sightseeing"
    budget = "0"  # euro
    multiple_locations = 1  # number of locations
    group = 4  # number of people
    duration = "any amount"
    activity_level = "moderate"  # low, moderate, high
        
    gen_response(location, activity_type, budget, multiple_locations, group, duration, activity_level)   
        
    # Get recommendation from AI
    # recommendation = get_ai_recommendation(location, activity_type, budget, multiple_locations, group, duration, activity_level)
    
    # write_to_file(recommendation)
    
    # print("\nAI Recommendation:\n", recommendation)


# Run the program
if __name__ == "__main__":
    get_user_input()
