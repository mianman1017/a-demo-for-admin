from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,render,redirect

# 自定义中间件

# 验证用户是否已经登录的中间件
class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        # 排除那些不需要登录就能访问的页面
        # request.path_info获取当前用户请求的URL
        if request.path_info=='/login/':
            return

        # 如果方法中没有返回值，则可以继续通过
        # 如果有返回值,则不能继续通过

        # 读取当前用户访问的session信息，如果能读到，说明已经登录
        # 检查用户是否已经登录，如果未登录，则跳转回登录页面
        # 获取用户请求中的cookie随机字符串，看看session中有没有
        info = request.session.get("info")
        if not info:
            return redirect('/login/')
        else:
            return

