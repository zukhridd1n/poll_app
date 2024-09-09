from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Account


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1  = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise ValidationError('Username already exists')
        return value


    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password': 'Passwords must be match'})
        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email')

