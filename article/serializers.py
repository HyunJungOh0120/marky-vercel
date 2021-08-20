from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        print("create💚")
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("update", validated_data)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.url_address = validated_data.get("url_address", instance.url_address)
        instance.image = validated_data.get("image", instance.image)
        instance.user = validated_data.get("user", instance.user)

        instance.slug = validated_data.get("slug", instance.slug)
        instance.file_url = validated_data.get("file_url", instance.file_url)
        instance.category = validated_data.get("category", instance.category)
        instance.save()
        return instance
