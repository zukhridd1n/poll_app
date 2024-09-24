from django.urls import include, path
from rest_framework.routers import DefaultRouter

from poll.views import ChoiceViewSet, PollViewSet, VoteView

router = DefaultRouter()
router.register("votes", VoteView, basename="vote")
router.register("choice", ChoiceViewSet, basename="choice")
router.register("", PollViewSet)

app_name = "poll"

urlpatterns = [
    # path('', PollsView.as_view(), name='poll-list'),
    # path('<int:pk>/', PollView.as_view(), name='poll-detail'),
    path("", include(router.urls)),
]
