from rest_framework import serializers
from .models import Challenge, Participation, Progress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ['participation']

class ParticipationSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ['user', 'challenge', 'join_date']

class ChallengeSerializer(serializers.ModelSerializer):
    participations = ParticipationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Challenge
        fields = '__all__'
