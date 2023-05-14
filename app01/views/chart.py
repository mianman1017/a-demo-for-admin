from django.shortcuts import render

# 数据统计页面
def chart_list(request):
    return render(request,'chart_list.html')
