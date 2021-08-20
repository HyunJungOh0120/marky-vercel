from django.urls import path
from .views import ArticleAPIView, OneArticleAPIView


urlpatterns = [
    path('', ArticleAPIView.as_view()),
    
    path('<int:id>', OneArticleAPIView.as_view()),

]
