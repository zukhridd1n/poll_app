from django.urls import path

from poll.views import PollsView, PollView,  ChoicesView, ChoiceView

urlpatterns = [
    path('', PollsView.as_view(), name='poll-list'),
    path('<int:pk>/', PollView.as_view(), name='poll-detail'),
    path('choices/', ChoicesView.as_view(), name='choice-list'),
    path('choice/<int:pk>/', ChoiceView.as_view(), name='choice-detail')
]