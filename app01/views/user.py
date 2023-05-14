from django.shortcuts import render, redirect
from app01 import models
from django import forms
from app01.utils.Pagination import Pagination
from app01.utils.BootStrap import BootStrapModelForm
from app01.utils.form import UserModelFrom

def user_list(request):
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    # 添加用户
    if request.method == "GET":
        form = UserModelFrom()
        return render(request, 'user_add.html', {"form": form})
    else:
        # 用户POST提交数据，数据校验
        form = UserModelFrom(data=request.POST)
        if form.is_valid():
            # 默认保存的是用户输入人的所有数据
            # 可额外添加: form.instance.字段名 = 值
            form.save()
            return redirect('/user/list/')
        else:
            return render(request, 'user_add.html', {"form": form})


def user_delete(request):
    # 获取nid
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):
    # 编辑用户
    editrow = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelFrom(instance=editrow)
        return render(request, 'user_edit.html', {"form": form})
    else:
        form = UserModelFrom(data=request.POST, instance=editrow)
        if form.is_valid():
            form.save()
            return redirect('/user/list/')
        else:
            return render(request, 'user_edit.html', {"form": form})
