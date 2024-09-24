from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer

from account.models import Account, AccountProfile, Interest


class AccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    # email = serializers.EmailField(required=True, allow_null=False)
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError("Passwords must be match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        account: Account = super().create(validated_data)
        account.set_password(validated_data["password"])
        account.save()
        return account

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
        )
        extra_kwargs = {
            "email": {"required": True, "allow_null": False},
            "first_name": {"required": True, "allow_null": False},
            "last_name": {"required": True, "allow_null": False},
        }


class AccountProfileSerializer(ModelSerializer):
    passport_number = serializers.CharField(required=False)
    passport_letter = serializers.CharField(required=False)

    # interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, )
    # interests = InterestSerializer(many=True)
    class Meta:
        model = AccountProfile
        fields = ("city", "passport_number", "passport_letter", "interests")
        extra_kwargs = {
            "interests": {"required": False, "allow_null": True, "allow_empty": True},
            "city": {"required": False, "allow_null": True},
            "passport_number": {"required": False, "allow_null": True},
            "passport_letter": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance: AccountProfile):
        representation = super().to_representation(instance)
        representation["interests"] = InterestSerializer(
            instance.interests, many=True
        ).data
        return representation


class AccountDetialSeriaizer(ModelSerializer):
    profile = AccountProfileSerializer()
    avatar = ImageField()

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile",
            "avatar",
            "music",
            "rating",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_null": True},
            "first_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
            "profile": {"required": False, "allow_null": True},
        }

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)

    def update(self, instance, validated_data):
        profile = validated_data.pop("profile", None)
        super().update(instance, validated_data)
        account_profile: AccountProfile = instance.profile
        if profile:
            intrests = profile.pop("interests", None)
            for key, value in profile.items():
                setattr(account_profile, key, value)
            if intrests or isinstance(intrests, list):
                account_profile.interests.set(intrests)
            account_profile.save()
        return instance


class InterestSerializer(ModelSerializer):
    class Meta:
        model = Interest
        fields = ("id", "name", "slug")
        extra_kwargs = {
            "slug": {"required": False, "allow_null": True, "read_only": True},
        }


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "permissions")
