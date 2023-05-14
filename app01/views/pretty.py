from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.Pagination import Pagination
from app01.utils.BootStrap import BootStrapModelForm
from app01.utils.form import PrettyModelForm,PrettyEditModelForm


def pretty_list(request):
    # page = int(request.GET.get("page", 1))
    # list_size = 10  # 每页显示10条数据
    # list_start = (page - 1) * list_size
    # list_end = page * list_size

    # 搜索
    data_dict = {}
    search_data = request.GET.get("search", '')
    if search_data:
        data_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")

    # 分页
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }

    return render(request, 'pretty_list.html', context)


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


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})
    else:
        # 用户POST提交数据，数据校验
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            # 默认保存的是用户输入人的所有数据
            # 可额外添加: form.instance.字段名 = 值
            form.save()
            return redirect('/pretty/list/')
        else:
            return render(request, 'pretty_add.html', {"form": form})



def pretty_edit(request, nid):
    # 编辑靓号
    editrow = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=editrow)
        return render(request, 'pretty_edit.html', {"form": form})
    else:
        form = PrettyEditModelForm(data=request.POST, instance=editrow)
        if form.is_valid():
            form.save()
            return redirect('/pretty/list/')
        else:
            return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request):
    # 获取nid
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
