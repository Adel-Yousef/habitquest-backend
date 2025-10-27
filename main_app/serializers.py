from rest_framework import serializers
from .models import Challenge, Participation, Progress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    Progress = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    Participations = ParticipationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Challenge
        fields = '__all__'
