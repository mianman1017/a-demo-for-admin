from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.BootStrap import BootStrapModelForm

def depart_list(request):
    # 部门列表
    queryset = models.Department.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    # 添加部门
    if request.method == "GET":
        return render(request, 'depart_add.html')
    else:
        title = request.POST.get("title")
        print(title)
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")


def depart_delete(request):
    # 获取nid
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    # 修改部门
    if request.method == "GET":
        editrow = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"editrow": editrow})
    else:
        title = request.POST.get("title")
        models.Department.objects.filter(id=nid).update(title=title)
        return redirect("/depart/list/")
