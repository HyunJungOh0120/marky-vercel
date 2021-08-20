from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (ChangePasswordView, LoginView, LogoutView, RegisterView,
                    UserView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/',
         ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('info/', UserView.as_view())
]
