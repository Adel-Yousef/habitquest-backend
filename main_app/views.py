from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Challenge, Participation, Progress
from .serializers import ChallengeSerializer, ParticipationSerializer, ProgressSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)

User = get_user_model()

# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the HqbitQuest API!'}
        return Response(content)
    
    def post(self, request):
        data = request.data
        print(request.data)
        content = {
            'message': 'Welcome, you just posted to the HabitQuest!',
            'data': data
        }
        return Response(content)

class ChallengeIndex(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Challenge.objects.all()
        serializer = ChallengeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            serializer = ChallengeSerializer(data=request.data)
            
            if serializer.is_valid():
                # so the created_by still the user and doesnt go to null
                serializer.save(created_by=request.user)
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


class ParticipationsIndex(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        queryset = Participation.objects.filter(challenge=challenge_id)
        serializer = ParticipationSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, challenge_id):
        try:
            serializer = ParticipationSerializer(data=request.data)
            
            if serializer.is_valid():
                challenge = Challenge.objects.get(id=challenge_id)
                serializer.save(user=request.user, challenge=challenge)
                queryset = Participation.objects.filter(challenge=challenge_id)
                many_serializer = ParticipationSerializer(queryset, many=True)
                return Response(many_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ParticipationProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, participation_id):
        queryset = Progress.objects.filter(participation=participation_id)
        serializer = ProgressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, participation_id):
        try:
            participation = get_object_or_404(Participation, id=participation_id)

            serializer = ProgressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(participation=participation)
                queryset = Progress.objects.filter(participation=participation_id)
                many_serializer = ProgressSerializer(queryset, many=True)
                return Response(many_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeaveChallenge(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, challenge_id):
        try:
            challenge = get_object_or_404(Challenge, id=challenge_id)

            participation = get_object_or_404(Participation, challenge=challenge, user=request.user)
            participation.delete()

            user_participations = Participation.objects.filter(user=request.user)
            challenges_user_has_joined = Challenge.objects.filter(id__in=user_participations.values_list('challenge_id', flat=True))
            return Response({
                'message': f'User {request.user.username} left challenge {challenge_id}',
                'challenges_user_has_joined': ChallengeSerializer(challenges_user_has_joined, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# for the dashboard
class MyChallenges(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Challenge.objects.filter(created_by=request.user)
        serializer = ChallengeSerializer(queryset,many=True)
        return Response(serializer.data)

# for the dashboard   
class MyParticipations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Participation.objects.filter(user=request.user)
        serializer = ParticipationSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GetUsername(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)

class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password or not email:
            return Response(
                {"error": "Please provide a username, password, and email"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User Already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        return Response(
            {"id":user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED
        )
        