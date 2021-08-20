from memo.models import Memo
from django.contrib import admin
from .models import Memo

# Register your models here.


class MemoAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'article']


admin.site.register(Memo, MemoAdmin)
