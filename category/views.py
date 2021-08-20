from article.models import Article
from article.serializers import ArticleSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify.slugify import slugify


from .models import Category, CATEGORY_CHOICES
from .serializers import CategorySerializer


# Create your views here.
class ChoicesView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(CATEGORY_CHOICES)


class CategoryAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()

    def get(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        obj = qs.first()
        serializer = self.serializer_class(obj)

        article = Article.objects.filter(category=id)

        # has article
        article_serializer = ArticleSerializer(article, many=True)
        data = {
            "category": serializer.data,

            "articles": article_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()

        topic = request.data.get('topic')
        name = request.data.get('name')
        user = request.user.id
        slug = slugify(name)

        data = {
            'topic': topic,
            'name': name,
            'user': user,
            'slug': slug
        }
        serializer = self.serializer_class(instance=obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        qs = qs.filter(user=request.user.id)
        if not qs.exists():
            return Response({"message": "You cannot delete this category"})

        obj = qs.first()
        obj.delete()

        return Response({"message": "Category is removed"}, status=status.HTTP_204_NO_CONTENT)


class CategoriesAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()


# per user

    def get(self, request):

        user = request.user.id
        qs = self.queryset.filter(user=user)

        serializer = self.serializer_class(qs, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user.id
        topic = request.data.get('topic')
        name = request.data.get('name')

        slug = slugify(name)

        data = {
            'user': user,
            'topic': topic,
            'name': name,
            'slug': slug,

        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
