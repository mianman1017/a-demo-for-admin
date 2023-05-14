from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.BootStrap import BootStrapModelForm
from app01.utils.encrypt import md5


class UserModelFrom(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "gender", "age", "account", "create_time", "department"]


class PrettyEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # [方法二]验证mobile的输入格式
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile


class PrettyModelForm(BootStrapModelForm):
    # [方法一]验证mobile格式
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # [方法二]验证mobile的输入格式
    # 钩子，一定要会
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True是为了让密码不一致需要重新输入时原先输入的密码不清空，仍保留在输入框中
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        # 给密码进行MD5加密
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        # 返回什么，最终password的值就会更改为什么
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True是为了让密码不一致需要重新输入时原先输入的密码不清空，仍保留在输入框中
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 给密码进行MD5加密
        md5_pwd=md5(pwd)
        # 去数据库校验之前的密码和新输入的密码是否一致
        exists=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        # 返回什么，最终password的值就会更改为什么
        return confirm