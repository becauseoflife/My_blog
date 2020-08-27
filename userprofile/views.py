from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from .models import Profile


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


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存用户数据后立即登录并返回微博首页
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误，请重新输入！")
    elif request.method == "GET":
        user_register_form = UserRegisterForm()
        context = {
            'form': user_register_form
        }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用 GET 或 POST 方式请求数据！")


# 删除用户数据
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    # 验证登录用户和待删除用户是否相同
    if request.user == user:
        # 退出登录、删除数据并返回文章列表
        logout(request)
        user.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("你没有删除权限！")


# 编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改用户是否是用户本人
        if request.user != user:
            return HttpResponse('你没有权限修改此用户的信息')

        # 上传的文件保存在 request。FILES 中， 通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 如果 request。FILES 中存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("表单输入有误，请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        """
        实际上GET方法中不需要将profile_form这个表单对象传递到模板中去，
        因为模板中已经用Bootstrap写好了表单，
        所以profile_form并没有用到
        """
        context = {
            'profile_form': profile_form,
            'profile': profile,
            'user': user,
        }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用 GET 或 POST 请求~')