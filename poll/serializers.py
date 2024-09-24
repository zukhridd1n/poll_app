from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import Account
from account.serializers import (AccountDetialSeriaizer,
                                 AccountProfileSerializer, AccountSerializer)
from poll.models import Choice, Poll, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "question", "published", "author_id")


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "answer", "poll")


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "choice", "voted_by", "voted_at")
        extra_kwargs = {
            "choice": {"read_only": True},
            "voted_at": {"read_only": True},
            "voted_by": {"read_only": True},
        }


class PollPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(required=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), required=False
    )
