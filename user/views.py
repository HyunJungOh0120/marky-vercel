from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from user.models import MyUser

from .serializers import (ChangePasswordSerializer,
                          CookieTokenRefreshSerializer, LoginSerializer,
                          MyUserSerializer, RegisterSerializer)

# Create your views here.


class RegisterView(GenericAPIView):
    """
    POST api/user/register/
    """
    serializer_class = RegisterSerializer
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            newuser = serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserView(APIView):
    serializer_class = MyUserSerializer
    model = MyUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    POST api/user/login/
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class CookieTokenRefreshView(TokenRefreshView):
    """
    POST api/user/login/refresh/

    """
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    model = MyUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST api/user/logout/
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('success', status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

