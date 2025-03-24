from django.db import models
from django.contrib.auth.models import User
from api.models.Profile import Profile
from autoslug import AutoSlugField

from .Category import Category
from .Tag import Tag

import uuid

class Post(models.Model):
    '''
        id:             UUIDField       欄位，主鍵
        author:         ForeignKey      欄位，關聯 User
        studient_id:    CharField       欄位，學號
        category:       ForeignKey      欄位，關聯 Category
        tags:           ManyToManyField 欄位，關聯 Tag
        title:          CharField 欄位，標題
        content:        TextField 欄位，內容
        link:           URLField 欄位，連結
        views:          PositiveIntegerField 欄位，瀏覽次數
        liked_by:       ManyToManyField 欄位，關聯 User
        created_at:     DateTimeField 欄位，建立時間
        updated_at:     DateTimeField 欄位，更新時間
        slug:           AutoSlugField 欄位，Slug

    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    studient_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='學號')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category', verbose_name='類別')
    tags = models.ManyToManyField(Tag, related_name='tags', verbose_name='標籤')
    title = models.CharField(max_length=10, verbose_name='標題')
    content = models.TextField(verbose_name='內容')
    link = models.URLField(verbose_name='連結')
    views = models.PositiveIntegerField(default=0, verbose_name='瀏覽次數')
    liked_by = models.ManyToManyField(User, through='PostLike', related_name='liked_posts', verbose_name='喜歡數量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, verbose_name='Slug')

    def __str__(self):
        return self.title
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='案讚者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.user.username + ' like ' + self.post.title

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments', verbose_name='留言者')
    content = models.TextField(max_length=100, verbose_name='留言內容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.content