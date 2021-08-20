from django.db import models
from django.conf import settings

from article.models import Article

# Create your models here.


class Memo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text}'

    class Meta:
        db_table = 'memo'
        ordering = ['-created_at']
