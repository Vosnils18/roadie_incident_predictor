# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PredictionHistory, Incident

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['name', 'severity', 'probability']

class PredictionHistorySerializer(serializers.ModelSerializer):
    incident_types = IncidentSerializer(many=True, read_only=True)

    class Meta:
        model = PredictionHistory
        fields = ['id', 'user', 'date', 'incident_types']