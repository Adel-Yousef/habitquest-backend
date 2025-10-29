from django.urls import path
from .views import ChallengeIndex, MyParticipations, MyChallenges, ChallengeDetail


urlpatterns = [
    path('challenges/', ChallengeIndex.as_view(), name='challenges_index'),
    path('challenges/<int:challenge_id>/', ChallengeDetail.as_view(), name='challenge_detail'),
    path('my-challenges/<int:user_id>/', MyChallenges.as_view(), name='my_challenges'),
    path('my-participations/<int:user_id>/', MyParticipations.as_view(), name='my_participations')
]