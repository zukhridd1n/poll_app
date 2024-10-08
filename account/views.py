from click import group
from django.contrib.auth.models import Permission, Group
from django.core.serializers import serialize
from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from account.models import Account, Interest
from account.order import CustomOrderingFilter
from account.search import CustomSearchFilter
from account.serializers import AccountSerializer, InterestSerializer, AccountDetialSeriaizer, PermissionSerializer, \
    GroupSerializer


class AccountView(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all().order_by('id')
    serializer_class2 = AccountDetialSeriaizer
    my_tags = ('account',)
    filter_backends = (CustomSearchFilter, CustomOrderingFilter)
    search_fields = ('username', 'email', 'profile')
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        phone  = self.request.query_params.get('phone', None)
        interest  = self.request.query_params.get('interest', None)
        city  = self.request.query_params.get('city', None)
        if phone:
            queryset = queryset.filter(phone__contains=phone)
        if interest:
            queryset = queryset.filter(profile__interests__slug=interest)
        if city:
            queryset = queryset.filter(profile__city=city)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('phone', openapi.IN_QUERY, description='User Phone number filter', type=openapi.TYPE_STRING),
            openapi.Parameter('interest', openapi.IN_QUERY, description='User interest slug filter', type=openapi.TYPE_STRING),
            openapi.Parameter('city', openapi.IN_QUERY, description='User`s city  filter', type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def interests(self, *args, **kwargs):
        account = self.get_object()
        serializer = InterestSerializer(account.
        profile.interests.all(), many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, url_path='top-accounts')
    def top_accounts(self, *args, **kwargs):
        queryset = self.get_queryset()
        # queryset = queryset.filter(profile__interests__isnull=False).distinct()
        queryset = (
            queryset.annotate(interest_count=Count("profile__interests")).filter(interest_count__gt=0).order_by("-interest_count")
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    # create list -> AccountSerializer
    # detail, put, patch, delete -> AccountDetailSerializer
    def retrieve(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        if request.user == account:
            serializer = self.serializer_class2(data=request.data, instance=account)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            return Response(data={"message": "You cannot update this account"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        if request.user == account:
            serializer = self.serializer_class2(data=request.data, instance=account, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            return Response(data={"message": "You cannot update this account"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class InterestView(ViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    my_tags = ('interest',)


    def list(self, request):
        serializer = InterestSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        interest = get_object_or_404(Interest, pk=pk)
        serializer = self.serializer_class(instance=interest, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

class PermissionViewSet(ModelViewSet):
    my_tags = ('permission',)
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer


class GroupViewSet(ModelViewSet):
    my_tags = ('group',)
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer


    @action(detail=True, methods=['post'], url_path='permission')
    def add_permission_to_group(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        per_id = request.data.get('permissions', [])
        permissions = Permission.objects.filter(id__in=per_id)
        for permission in permissions:
            group.permissions.add(permission)
        group.save()
        return Response({"status": "permissions added"}, status=status.HTTP_200_OK)


