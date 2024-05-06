
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect,HttpResponse

# 路由中间件
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除不需要登录就能访问的页面
        # 获取当前用户请求的url request.path_info

        if request.path_info in ["/account/login","/image/code"]:

            return

        # 如果方法中没有返回值，返回None，继续后走
        # 如果有返回值，HttpResponse
        # 1.读取当前访问用户的session信息，如果读取到说明已经登录过，可以继续往后

        info_dict = request.session.get('info')
        print(info_dict)

        if info_dict:
            return

        return redirect('/account/login')