from memo.views import MemosAPIView, MemoAPIView
from django.urls import include, path


urlpatterns = [
    path('', MemosAPIView.as_view()),
    path('<int:id>', MemoAPIView.as_view())
]
