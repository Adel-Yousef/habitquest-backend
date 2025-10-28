from django.urls import path
from .views import ChallengeIndex, MyParticipations, ParticipationsIndex, MyChallenges


urlpatterns = [
    path('challenges/', ChallengeIndex.as_view(), name='challenges_index'),
    path('participations/', ParticipationsIndex.as_view(), name='participations_index'),
    path('my-challenges/<int:user_id>/', MyChallenges.as_view(), name='my_challenges'),
    path('my-participations/<int:user_id>/', MyParticipations.as_view(), name='my_participations')
]