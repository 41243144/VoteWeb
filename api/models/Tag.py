from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tag_create_user',
        verbose_name='建立者'
    )
    name = models.CharField(max_length=255, verbose_name='標籤名稱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='刪除時間')

    def __str__(self):
        return self.name