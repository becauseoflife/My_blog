from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleamed_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 用户
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中， 即实现了登录动作
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入~")
        else:
            return HttpResponse("账号或面膜输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {
            'form': user_login_form
        }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用 GET 或者 POST 方式请求数据")


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")


