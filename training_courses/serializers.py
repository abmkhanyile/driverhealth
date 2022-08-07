from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import TrainingDays, TrainingEvent


class TrainingDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingDays
        fields = '__all__'


class TrainingEventSerializer(serializers.ModelSerializer):
    slots = TrainingDaysSerializer(many=True)
    class Meta:
        model = TrainingEvent
        fields = [
            'comment',
            'slots',
        ]