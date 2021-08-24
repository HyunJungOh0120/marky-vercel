"""marky_django4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

class HomeView(APIView):
    def get(self, request):
        return Response({"message": "hi"})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('home', HomeView.as_view()),
    path('api/user/', include('user.urls')),
    path('api/articles/', include('article.urls')),
    path('api/memo/', include('memo.urls')),
    path('api/category/', include('category.urls'))


]


