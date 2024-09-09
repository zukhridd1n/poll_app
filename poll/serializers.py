from rest_framework import serializers

from account.models import Account
from poll.models import Poll, Choice, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'question', 'author', 'published')

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'answer', 'poll')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'poll', 'choice', 'vote_by')


class PollPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)


