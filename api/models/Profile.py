from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='使用者')
    studient_id = models.CharField(max_length=10, unique=True, verbose_name='學號')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='姓名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.user.username