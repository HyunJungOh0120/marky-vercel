from django.urls import path

from category.views import CategoriesAPIView, CategoryAPIView, ChoicesView

urlpatterns = [
    path('', CategoriesAPIView.as_view(), name='category-list'),
    path('<int:id>', CategoryAPIView.as_view(), name='category-detail'),
    path('choice/', ChoicesView.as_view())

]
