from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User
from journey.models import Journal
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import openai
import json

class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Create an empty journal for the user
        Journal.objects.create(user=user)
    
class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

