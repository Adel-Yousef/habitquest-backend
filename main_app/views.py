from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Challenge
from .serializers import ChallengeSerializer

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

       