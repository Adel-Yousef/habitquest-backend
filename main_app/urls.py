from django.urls import path
from .views import ChallengeIndex, MyParticipations, ParticipationsIndex, MyChallenges, ParticipationProgress, ChallengeDetail, LeaveChallenge


urlpatterns = [
    path('challenges/', ChallengeIndex.as_view(), name='challenges_index'),
    path('challenges/<int:challenge_id>/', ChallengeDetail.as_view(), name='challenge_detail'),
    path('challenges/<int:challenge_id>/participations/', ParticipationsIndex.as_view(), name='participations_index'),
    path('participations/<int:participation_id>/progress/', ParticipationProgress.as_view(),name='participation_progress'),
    path('challenges/<int:challenge_id>/leave/<int:user_id>/', LeaveChallenge.as_view(), name='leave_challenge'),
    path('my-challenges/<int:user_id>/', MyChallenges.as_view(), name='my_challenges'),
    path('my-participations/<int:user_id>/', MyParticipations.as_view(), name='my_participations')
]