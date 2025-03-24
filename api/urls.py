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

# Create a router and register our viewset with it.
# The API URLs are now determined automatically by the router.
router = DefaultRouter()
router.register(r'profile', ProfileView, basename='profile')
router.register(r'post', PostView, basename='post')
router.register(r'category', CategoryView, basename='category')
router.register(r'tag', TagView, basename='tag')
router.register(r'comment', CommentView, basename='comment')

urlpatterns = [
    path('', include(router.urls)),

]