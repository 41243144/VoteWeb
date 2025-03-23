from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:page>.html', views.pages, name='pages'),
]

# 文章相關
urlpatterns += [
    # 我要刊登
    path('articles/', views.articles, name='articles'),
    # 我的文章
    path('accounts/article-manager/', views.article_manager, name='article_manager'),
    # 文章編輯
    path('accounts/edit-article/<str:post_id>/', views.edit_article, name='edit_article'),
    # 所有文章
    path('articles_list/', views.articles_list, name='articles_list'),
    # 文章內容
    path('articles_list/<str:slug>/', views.article, name='article'),
    # 排行榜
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]

urlpatterns += [
    path('accounts/profile/', views.profile, name='profile'),
]