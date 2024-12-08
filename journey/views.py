from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import JourneyUpdateSerializer, JourneySerializer, JourneyGenerateSerializer, JourneyGenerateResponseSerializer
from .models import Journey
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import openai
import json
import urllib.parse
# Create your views here.
# class JourneyCreateAPIView(generics.ListCreateAPIView):
#     queryset = Journey.objects.all()
#     serializer_class = JourneySerializer


class JourneyCreateAPIView(generics.CreateAPIView):
    serializer_class = JourneySerializer


class JourneyUpdateAPIView(generics.UpdateAPIView):
    queryset = Journey.objects.all()
    serializer_class = JourneyUpdateSerializer


class JourneyGenerateAPIView(APIView):
    def __get_google_maps_link(self, location_name: str, city: str):
        base_url = "https://www.google.com/maps/search/"
        query = f"{location_name}, {city}"
        encoded_query = urllib.parse.quote(query)
        return f"{base_url}{encoded_query}"

    def __generate_journey(self, data: dict):
        initial_msg = f"""Based on the input generate an activity recommendation in JSON format; For each activity it should be a JSON, so the final response should be a list of JSONs:
        {{
            "name_of_location": "string",
            "description": "string",
            "budget_breakdown": "string",
            "wellbeing_impact": "string",
            "tags": ["string"],
        }}
        In the "wellbeing_impact" field you have to talk about how it possitively affects the individual's mental and physical health. Make sure you use a rich vocabulary for this section.
        In the "name_of_location" field you have to talk about the specific name of the location but dont also include the city name.
        The budget breakdown should be contain the cost of the activity. Make sure to take into account the user's total budget
        Make sure the location is the same as the one provided in the input.
        In the "tags" field you have to include the tags that describe the activity. For example, if the activity is "hiking", you can include the tag "outdoor" or "nature". Maximum 3 tags
        """

        prompt = f"""
        Can you recommend 3 different activities in {data['location']} based on the following factors:
        - Type: {data['activity_type']}
        - Budget: {data['budget']}
        - Group size: {data['group_size']}
        - Duration: {data['duration']}
        - Level of physical activity: {data['level_of_physical_activity']}
        - Additional information: {data['additional_information']}        
        """

        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for higher-quality responses
            messages=[
                {"role": "system", "content": initial_msg},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7,
        )

        # print(response.choices[0].message.content)
        try:
            print(f"{response.choices[0].message.content.strip()=}")
            result_json = json.loads(response.choices[0].message.content.strip())

            for result in result_json:
                result["maps_link"] = self.__get_google_maps_link(result["name_of_location"], "Cluj-Napoca")

        except json.JSONDecodeError:
            result_json = {"error": "Invalid JSON format returned by AI."}

        return result_json

    def post(self, request):
        serializer = JourneyGenerateSerializer(data=request.data)

        if serializer.is_valid():
            generated_journey_json = self.__generate_journey(serializer.validated_data)
            print(f"{generated_journey_json=}")
            journey_serializer = JourneyGenerateResponseSerializer(data=generated_journey_json, many=True)

            if journey_serializer.is_valid():
                return Response(journey_serializer.validated_data, status=201)
            return Response(journey_serializer.errors, status=400)
        return Response(serializer.errors, status=400)
