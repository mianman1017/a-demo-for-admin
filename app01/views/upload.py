from django.shortcuts import render,HttpResponse

def upload_list(request):
    if request.method=="GET":
        return render(request,'upload_list.html')
    else:
        file_object=request.FILES.get("avatar")
        # 注意，file_object.name只适用于图片
        print(file_object.name)
        # chunk是文件的一块一块的数据
        f=open(file_object.name,mode='wb')
        # 一块一块的将上传的文件写入以file_object.name命名的文件中
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('success')