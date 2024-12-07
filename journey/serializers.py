from .models import Journey, Journal
from rest_framework import serializers



class JourneySerializer(serializers.ModelSerializer):
    # journal_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Journey
        fields = "__all__"
        
    # def create(self, validated_data):
    #     journal_id = validated_data.pop('journal_id')
    #     try:
    #         journal = Journal.objects.get(id=journal_id)
    #     except Journal.DoesNotExist:
    #         raise serializers.ValidationError({"journal_id": "Journal not found."})
        
    #     # Create and return the JourneyEntry
    #     return Journey.objects.create(journal=journal, **validated_data)
        
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
    
# class JourneyEntrySerializer

class JournalSerializer(serializers.ModelSerializer):
    journeys = JourneySerializer(many=True, read_only=True)
    class Meta:
        model = Journal
        fields = ["journal_id", "user", "journeys"]