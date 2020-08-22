from django.shortcuts import render

# Create your views here.

# 导入HTTPResponse 模块
from django.http import HttpResponse
# 导入数据模型 ArticlePost
from .models import ArticlePost


# 视图函数
# 文章列表
def article_list(request):
    # return HttpResponse('Hello World!');
    # 取出所有的文章
    all_article = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {
        'all_article': all_article
    }
    # render 函数：载入模板 返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 需要传递给模板的对象
    context = {
        'article': article
    }
    # 载入模板，并返回 context对象
    return render(request, 'article/detail.html', context)