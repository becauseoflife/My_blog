# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile


# 登录表单， 继承了forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 用户注册表单
class UserRegisterForm(forms.ModelForm):
    # 复写用户的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码检验是否一致
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("两次输入的密码不一致，请重新输入！")


# Profile 表单类
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')