from django.urls import path
from .views import ChallengeIndex


urlpatterns = [
    path('challenges/', ChallengeIndex.as_view(), name='challenge_index'),
]