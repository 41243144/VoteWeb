from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    '''
        create_user:    ForeignKey 欄位，關聯 User
        name:           CharField  欄位，類別名稱
        created_at:     DateTimeField 欄位，建立時間
        updated_at:     DateTimeField 欄位，更新時間

        Meta:
            verbose_name: 類別
            verbose_name_plural: 類別
            ordering: ['-created_at']

        __str__: 用物件的 name 來表示物件
    '''
    create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='category_create_user',
        verbose_name='建立者'
    )
    name = models.CharField(max_length=255, verbose_name='類別名稱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.name