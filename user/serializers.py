
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'last_login', 'email', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                {'username': 'The username should only contain alphanumeric characters'})

        user = MyUser.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError({
                'email': 'This email is already used'
            })

        return attrs

    def create(self, validated_data):
        """
        Create and return a new user, given the validated data.
        """
        return MyUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['username'] = user.username
        return token


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\'')


class ChangePasswordSerializer(serializers.Serializer):
    model = MyUser
    """
    Serializer for password change endpoint
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    # def validate_new_password(self, value):
    #     validate_password(value)
    #     return value
