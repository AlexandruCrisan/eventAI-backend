from rest_framework import serializers
from .models import User
from journey.serializers import JournalSerializer

# class RecommendationInputSerializer(serializers.Serializer):
#     budget = serializers.IntegerField()
#     area = serializers.CharField(max_length=255)
#     duration = serializers.IntegerField()

# class RecommendationOutputSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     budget_breakdown = serializers.CharField()
#     wellbeing_impact = serializers.CharField()
    

class UserSerializer(serializers.ModelSerializer):
    journal = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "journal"]
        
    def get_journal(self, obj):
        journal = obj.journal
        return JournalSerializer(journal).data