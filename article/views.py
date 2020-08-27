from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

# 导入HTTPResponse 模块
from django.http import HttpResponse
# 导入数据模型 ArticlePost
from .models import ArticlePost
# 引入Markdown模块
import markdown
# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入分页模块
from django.core.paginator import Paginator


# 视图函数
# 文章列表
def article_list(request):
    # return HttpResponse('Hello World!');
    # 取出所有的文章
    # all_article = ArticlePost.objects.all()

    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        all_article = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        all_article = ArticlePost.objects.all()
        order = 'normal'


    # 每页显示 1 篇文章
    pageinator = Paginator(all_article, 3)
    # 获取 URL 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    page_articles = pageinator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'page_articles': page_articles,
        'order': order
    }
    # render 函数：载入模板 返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    # 阅读量
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将Markdown语法渲染成HTML样式
    article.body_content = markdown.markdown(article.body_content,
                                             extensions=[
                                                 # 包含 缩写、表格等常用扩展
                                                 'markdown.extensions.extra',
                                                 # 语法高亮扩展
                                                 'markdown.extensions.codehilite',
                                                 # 目录扩展
                                                 'markdown.extensions.toc',
                                             ])

    # print(article.body_content)

    # 需要传递给模板的对象
    context = {
        'article': article
    }
    # 载入模板，并返回 context对象
    return render(request, 'article/detail.html', context)


# 写文章视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的需求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户作为作者 >>>> 修改为登录用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成返回到文章列表
            return redirect("article:article_list")
        # 数据不合法，则返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {
            "article_post_form": article_post_form
        }
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用 .delete() 方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body_content字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者用户
    if request.user != article.author:
        return HttpResponse("抱歉！你无权修改这篇文章！")

    # 判断用户是否是 POST 提交数据表单
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body_content 数据并保存
            article.title = request.POST['title']
            article.body_content = request.POST['body_content']
            article.save()
            # 完成修改后，返回修改后的文章。需要传入文章的 id
            return redirect("article:article_detail", id=id)
        # 如果用户提交的数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象转进去，以便提取旧内容
        context = {
            "article": article,
            "article_post_form": article_post_form
        }
        # 返回模板
        return render(request, 'article/update.html', context)
