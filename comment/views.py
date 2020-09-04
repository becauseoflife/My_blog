from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.middleware import clickjacking

# Create your views here.


# 文章评论
from django.views.decorators.clickjacking import xframe_options_exempt
from notifications.signals import notify

from article.models import ArticlePost
from comment.forms import CommentForm
from comment.models import Comment

"""
    NGINX中可以设置 X-Frame-Options响应头
    X-Frame-Options 响应头有三种不同的选项：
    ALLOW-FROM：页面地址允许frame加载。 
    SAMEORIGIN：页面地址只能被同源域名页面嵌入到frame中；
    DENY：页面地址不能被嵌入到任何frame中；
    在django中：
    django中对应这三种类型：
    xframe_options_exempt
    xframe_options_sameorigin
    xframe_options_deny
    引入地址：
    from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin, xframe_options_deny
    使用：
    在 对应接口上添加对应的 装饰器 ， 使用xframe_options_exempt可避免问题的发生
"""


@xframe_options_exempt
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级， 则转为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复的人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # 新增代码，给其他用户发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复你了',
                        target=article,
                        action_objext=new_comment
                    )

                # return HttpResponse('200 OK')
                return JsonResponse({
                    'code': "200 OK",
                    'new_comment_id': new_comment.id
                })

            new_comment.save()

            # 新增代码， 给管理员用户发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment
                )

            # 新增代码，添加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            # 修改redirect参数
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)

    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受 POST 请求")
