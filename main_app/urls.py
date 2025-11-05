from django.urls import path
from .views import ChallengeIndex, MyParticipations, ParticipationsIndex, MyChallenges, ParticipationProgress, ChallengeDetail, LeaveChallenge, Home, SignupUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('challenges/', ChallengeIndex.as_view(), name='challenges_index'),
    path('challenges/<int:challenge_id>/', ChallengeDetail.as_view(), name='challenge_detail'),
    path('challenges/<int:challenge_id>/participations/', ParticipationsIndex.as_view(), name='participations_index'),
    path('participations/<int:participation_id>/progress/', ParticipationProgress.as_view(),name='participation_progress'),
    path('challenges/<int:challenge_id>/leave/', LeaveChallenge.as_view(), name='leave_challenge'),
    path('my-challenges/', MyChallenges.as_view(), name='my_challenges'),
    path('my-participations/', MyParticipations.as_view(), name='my_participations'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupUserView.as_view(), name='signup'),
]