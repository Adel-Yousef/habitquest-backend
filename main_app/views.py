from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Challenge, Participation, Progress
from .serializers import ChallengeSerializer, ParticipationSerializer, ProgressSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class ChallengeIndex(APIView):
    def get(self, request):
        queryset = Challenge.objects.all()
        serializer = ChallengeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            serializer = ChallengeSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChallengeDetail(APIView):
    def get(self, request, challenge_id):
        try:
            queryset = get_object_or_404(Challenge, id=challenge_id)
            serializer = ChallengeSerializer(queryset)
            participations_challenge_has = Participation.objects.filter(challenge=challenge_id)
            data = serializer.data
            data['participations'] = ParticipationSerializer(participations_challenge_has, many=True).data
            return Response(data)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, challenge_id):
        try:
            queryset = get_object_or_404(Challenge, id=challenge_id)
            serializer = ChallengeSerializer(queryset, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, challenge_id):
        try:
            queryset = get_object_or_404(Challenge, id=challenge_id)
            queryset.delete()
            return Response({'message': f'Challenge {challenge_id} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class LeaveChallenge(APIView):
    def delete(self, request, challenge_id, user_id):
        try:
            challenge = get_object_or_404(Challenge, id=challenge_id)
            user = get_object_or_404(User, id=user_id)

            participation = get_object_or_404(Participation, challenge=challenge, user=user)
            participation.delete()

            user_participations = Participation.objects.filter(user_id=user_id)
            challenges_user_has_joined = Challenge.objects.filter(id__in=user_participations.values_list('challenge_id', flat=True))
            return Response({
                'message': f'User {user_id} left challenge {challenge_id}',
                'challenges_user_has_joined': ChallengeSerializer(challenges_user_has_joined, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# for the dashboard
class MyChallenges(APIView):
    def get(self, request, user_id):
        queryset = Challenge.objects.filter(created_by_id=user_id)
        serializer = ChallengeSerializer(queryset,many=True)
        return Response(serializer.data)

# for the dashboard   
class MyParticipations(APIView):
    def get(self, request, user_id):
        queryset = Participation.objects.filter(user_id=user_id)
        serializer = ParticipationSerializer(queryset, many=True)
        return Response(serializer.data)
    

