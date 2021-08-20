from category.models import Category
from django.conf import settings
from django.db import models


# Create your models here.


class Article(models.Model):

    url_address = models.CharField(max_length=300)
    title = models.CharField(max_length=300, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    file_url = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.url_address}'

    class Meta:
        db_table = 'article'
        ordering = ['-created_at']


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)
