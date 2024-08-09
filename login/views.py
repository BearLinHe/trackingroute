
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import Users


def login(request):

    if request.method == 'GET':
        # 请求页面 有没有cookie 和 session
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
                # return HttpResponseRedirect('/index')
            if  username=='':
                if 'username' in request.session:
                    username= request.session.get('username')
                return HttpResponseRedirect('/login')
        data = {
            'username': '',
            'password': '',
            'error': '',
        }

        return render(request, 'login.html', data)
    if request.method == 'POST':
        # 获取用户输入的账号密码
        print('22')
        mobile=request.POST.get('mobile')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        # 从数据库里对比账号密码
        from index.models import User
        # 判断账号密码是否有问题
        result = Users.objects.filter(mobile=mobile, password=password)
        # print(f'mobile{mobile}')

        username=''
        if result:
           username = result.values()[0]['username']
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
        print(f'username{len(list(result))}')
        if  username=='' or  len(list(result))==0:
            return HttpResponseRedirect('/')

        if result:
            # 账号密码正确记录登录的信息
            print(result.values()[0]['username'])
            username = result.values()[0]['username']
            mobile = result.values()[0]['mobile']
            print(mobile)
            # 重定向到用户页面，携带username数据
            Response = HttpResponseRedirect('/wlgl')
            #
            # request.session.
            Response.set_cookie('username', username, 60 * 60)

            return HttpResponseRedirect('/wlgl')
        # 返回到个人中心

           # return render(request, 'person.html', Response)
        else:
                    # 当账号密码不正确的时候
            if request.COOKIES.get('username'):

                error ="您已经成功登录"
            else:
                error = "请正确的输入用户名和密码"
                messages.error(request, error)
                return HttpResponseRedirect('/')


