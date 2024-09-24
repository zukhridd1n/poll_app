from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from yaml import serialize

from config.search import PollSearchFilter
from poll.filters import AnswerFilterBackend
from poll.models import Choice, Poll, Vote
from poll.order import ChoiceOrderingFilter
from poll.serializers import ChoiceSerializer, PollSerializer, VoteSerializer

#
# class PollsView(APIView):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (BasicAuthentication, TokenAuthentication)
#     my_tags = ('poll',)
#
#
#     def get(self, request):
#         polls  = Poll.objects.filter(author=request.user)
#         serializer = PollSerializer(polls, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         request_body=PollSerializer,
#         operation_description='This endpoint for creating a poll'
#     )
#
#     def post(self, request):
#         serializer = PollSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class PollView(APIView):
#     my_tags = ('poll',)
#
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(poll)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(instance=poll, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data={"message": "Object successfully updated"}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(instance = poll, data = request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             for key, value in data.items():
#                 setattr(poll, key, value)
#             poll.save()
#             return Response(data={"message": "Object successfully updated"}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def delete(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         poll.delete()
#         return Response(data={"massage" : "Object successfully delete "} ,status=status.HTTP_202_ACCEPTED)


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all().order_by("id")
    serializer_class = PollSerializer
    # filter_backends = [PollSearchFilter]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("question", "published")
    my_tags = ("poll",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        super().perform_create(serializer)


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, ChoiceOrderingFilter)
    search_fields = ("poll ",)
    #
    # filter_backends = (DjangoFilterBackend, AnswerFilterBackend)
    # filterset_fields = ('answer',)

    def get_queryset(self):
        queryset = super().get_queryset()
        answer = self.request.query_params.get("answer", None)

        if answer:
            queryset = queryset.filter(answer__iendswith=f"{answer}")

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "answer",
                openapi.IN_QUERY,
                description="Answer end word with filter",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # pagination_by = 1

    my_tags = ("choice",)

    @action(detail=True, methods=["post"])
    def vote(self, *args, **kwargs):
        choice = self.get_object()
        user = self.request.user
        vote = Vote.objects.create(choice=choice, poll=choice.poll, voted_by=user)
        serializer = VoteSerializer(vote)
        return Response(data=serializer.data)

    def perform_create(self, serializer):
        super().perform_create(serializer)


class VoteView(ViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    my_tags = ("vote",)

    @action(methods=["POST"], detail=False, url_path="top-votes")
    def top_votes(self, *args, **kwargs):
        queryset = Poll.objects.annotate(vote_count=Count("votes")).order_by(
            "-vote_count"
        )[3:]
        serializer = PollSerializer(queryset, many=True)
        return Response(data=serializer.data)

    def list(self, request):
        serializer = VoteSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        vote = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(vote)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        vote = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        vote = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        vote = get_object_or_404(self.queryset, pk=pk)
        vote.delete()
        return Response(status=status.HTTP_200_OK)
