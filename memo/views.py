from .models import Memo
from rest_framework.views import APIView
from .serializers import MemoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions

# Create your views here.


class MemoAPIView(APIView):
    serializer_class = MemoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Memo.objects.all()

    def get(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        qs = self.queryset.filter(pk=id)

        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()

        article = request.data.get('article')
        text = request.data.get('text')
        user = request.user.id

        data = {
            'article': article,
            'text': text,
            'user': user

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
            return Response({"message": "You cannot delete this memo"})

        obj = qs.first()
        obj.delete()

        return Response({"message": "Memo is removed"}, status=status.HTTP_204_NO_CONTENT)


class MemosAPIView(APIView):
    serializer_class = MemoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Memo.objects.all()

    def get(self, request):
        article = self.request.query_params.get('article')

        if article is not None:
            queryset = self.queryset.filter(article__id=article)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        article = request.data.get('article')
        text = request.data.get('text')
        user = request.user.id

        data = {
            'article': article,
            'text': text,
            'user': user
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        memo = serializer.data

        return Response(memo, status=status.HTTP_201_CREATED)
