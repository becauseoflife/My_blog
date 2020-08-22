
from django.urls import path, include

import article.views

# 正在部署的应用名称
app_name = 'article'

urlpatterns = [
    path('article_list', article.views.article_list, name='article_list'),
    path('article_detail/<int:id>/', article.views.article_detail, name='article_detail')
]