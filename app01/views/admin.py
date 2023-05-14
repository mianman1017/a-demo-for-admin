from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):

    # 搜索
    data_dict = {}
    search_data = request.GET.get("search", '')
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'searchdata': search_data
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    if request.method == "GET":
        form = AdminModelForm()

        return render(request, 'admin_add.html', {"form": form})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        return render(request, 'admin_add.html', {"form": form})


def admin_edit(request, nid):
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('admin/list/')

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {"form": form})
    else:
        form = AdminEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        return render(request, 'admin_edit.html', {"form": form})


def admin_delete(request):
    nid = request.GET.get("nid")
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('admin/list/')

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'admin_reset.html', {"form": form})
    else:
        form = AdminResetModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('admin/list/')

        return render(request, 'admin_reset.html', {"form": form})
