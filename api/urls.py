from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileView,
    PageNumberPagination,
    PostView, 
    CategoryView, 
    TagView,
    CommentView
)

router = DefaultRouter()
router.register(r'profile', ProfileView, basename='profile')
router.register(r'post', PostView, basename='post')
router.register(r'category', CategoryView, basename='category')
router.register(r'tag', TagView, basename='tag')
router.register(r'comment', CommentView, basename='comment')

urlpatterns = [
    path('', include(router.urls)),

]