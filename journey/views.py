from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import JourneySerializer, JourneyGenerateSerializer, JourneyGenerateResponseSerializer
from .models import Journey
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import openai
import json
# Create your views here.
# class JourneyCreateAPIView(generics.ListCreateAPIView):
#     queryset = Journey.objects.all()
#     serializer_class = JourneySerializer

class JourneyCreateAPIView(generics.CreateAPIView):
    serializer_class = JourneySerializer
    
class JourneyGenerateAPIView(APIView):
    def __generate_journey(self, data: dict):
        initial_msg = f"""Based on the input generate an activity recommendation in JSON format; For each activity it should be a JSON, so the final response should be a list of JSONs:
        {{
            "name_of_location": "string",
            "description": "string",
            "budget_breakdown": "string",
            "wellbeing_impact": "string"
        }}
        In the "wellbeing_impact" field you have to talk about how it possitively affects the individual's mental and physical health.
        In the "name_of_location" field you have to talk about the specific name of the location.
        The budget breakdown should be contain the cost of the activity and also include the currency . Make sure to take into account the user's total budget
        Make sure the location is the same as the one provided in the input.
        """
        
        prompt = f"""
        Can you recommend 3 different activities in {data['location']} based on the following factors:
        - Type: {data['activity_type']}
        - Budget: {data['budget']}
        - Group size: {data['group_size']}
        - Duration: {data['duration']}
        - Level of physical activity: {data['level_of_physical_activity']}
        """
        
        client = openai.OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for higher-quality responses
            messages=[
                {"role": "system", "content": initial_msg},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        
        # print(response.choices[0].message.content)
        try:
            result_json = json.loads(response.choices[0].message.content.strip())
            # print(f"{result_json=}")
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