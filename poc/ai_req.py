import requests
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI API Configuration
API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPEN_API_KEY")  # Replace with your OpenAI API key

# Function to send the prompt to the AI


def get_ai_recommendation(location, activity_type, budget, multiple_locations, group, duration, activity_level):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt
    prompt = f"""
    Can you recommend an activity in {location} based on the following factors:
    - Type: {activity_type}
    - Budget: {budget}
    - Multiple Locations: {multiple_locations}
    - Group: {group}
    - Duration: {duration}
    - Level of physical activity: {activity_level}
    """

    # API Payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that suggests activities based on given factors."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    # Send Request
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        print(response.text)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# User Input


def get_user_input():
    location = "Cluj-Napoca"
    activity_type = "hiking"
    budget = "50"  # euro
    multiple_locations = 2  # number of locations
    group = 4  # number of people
    duration = "1 day"
    activity_level = "moderate"  # low, moderate, high

    # Get recommendation from AI
    recommendation = get_ai_recommendation(location, activity_type, budget,
                                           multiple_locations, group, duration, activity_level)
    print("\nAI Recommendation:\n", recommendation)


# Run the program
if __name__ == "__main__":
    get_user_input()
