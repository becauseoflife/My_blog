from django.shortcuts import render

# Create your views here.

# 导入HTTPResponse 模块
from django.http import HttpResponse
# 导入数据模型 ArticlePost
from .models import ArticlePost

# 视图函数
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
