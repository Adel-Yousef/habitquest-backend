from django.urls import path
from .views import ChallengeIndex, ParticipationsIndex


urlpatterns = [
    path('challenges/', ChallengeIndex.as_view(), name='challenges_index'),
    path('participations/', ParticipationsIndex.as_view(), name='participations_index'),
    
]