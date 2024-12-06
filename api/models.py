from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass    

class Journey(models.Model):
    class PysicalActivityLevelChoices(models.TextChoices):
        LOW = "low"
        MODERATE = "moderate"
        HIGH = "high"
    
    journey_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journeys")
    name_of_location = models.CharField(max_length=255)
    description = models.TextField()
    budget_breakdown = models.CharField(max_length=255)
    wellbeing_impact = models.CharField(max_length=255)
    # physical_activity_level = models.CharField(max_length=20, choices=PysicalActivityLevelChoices.choices)

    def __str__(self):
        return self.name_of_location