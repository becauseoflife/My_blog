
from django.urls import path, include

import article.views

# 正在部署的应用名称
from article import views

app_name = 'article'

urlpatterns = [
    path('article_list', article.views.article_list, name='article_list'),
    path('article_detail/<int:id>/', article.views.article_detail, name='article_detail'),
    path('article_create/', article.views.article_create, name='article_create'),
    path('article_delete/<int:id>/', article.views.article_delete, name='article_delete'),
    path('article_update/<int:id>/', article.views.article_update, name='article_update'),
    # 安全删除文章
    path('article_safe_delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    # 类视图 详情
    path('detail_view/<int:pk>/', views.ArticleDetailView.as_view(), name='detail_view'),
    path('create_view/', views.ArticleCreateView.as_view(), name='create_view'),
]