from rest_framework import serializers
from .models import Challenge, Participation, Progress
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ['participation']

class ParticipationSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    challenge_title = serializers.CharField(source='challenge.title',read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ['user', 'challenge', 'join_date']

class ChallengeSerializer(serializers.ModelSerializer):
    participations = ParticipationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Challenge
        fields = '__all__'
