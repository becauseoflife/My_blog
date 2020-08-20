
from django.urls import path, include

import article.views

urlpatterns = [
    path('article_list', article.views.article_list, name='article_list')
]