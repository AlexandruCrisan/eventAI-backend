from rest_framework import serializers
from .models import Journey, User

class RecommendationInputSerializer(serializers.Serializer):
    budget = serializers.IntegerField()
    area = serializers.CharField(max_length=255)
    duration = serializers.IntegerField()

class RecommendationOutputSerializer(serializers.Serializer):
    name = serializers.CharField()
    budget_breakdown = serializers.CharField()
    wellbeing_impact = serializers.CharField()
    
class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"
        
class JourneyGenerateSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255)
    activity_type = serializers.CharField(max_length=255)
    budget = serializers.CharField(max_length=255)
    group_size = serializers.CharField(max_length=255)
    duration = serializers.CharField(max_length=255)
    level_of_physical_activity = serializers.ChoiceField(choices=Journey.PysicalActivityLevelChoices.choices)

class JourneyGenerateResponseSerializer(serializers.Serializer):
    name_of_location = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    budget_breakdown = serializers.CharField(max_length=255)
    wellbeing_impact = serializers.CharField(max_length=255) 

class UserSerializer(serializers.ModelSerializer):
    journeys = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "journeys"]
        
    def get_journeys(self, obj):
        journeys = obj.journeys.all()  # Access related `journeys`
        return JourneySerializer(journeys, many=True).data