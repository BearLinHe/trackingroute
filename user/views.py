import re

from django.contrib import messages
from django.contrib.sites import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from pip._vendor.requests import Response

from index.models import Users, label


def regsvr(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    compassword = request.POST.get('compassword', '')
    email = request.POST.get('email', '')
    gender = request.POST.get('is_gender', '')
    mobile = request.POST.get('mobile', '')
    qq = request.POST.get('qq', '')
    yhqx = request.POST.get('yhqx', '')
    wechat = request.POST.get('wechat', '')
    users = Users.objects.filter(mobile=mobile)
    strmsg=""
    info = {}
    if gender == 'on':
        is_gender = '男'
    else:
        is_gender = '女'
    if username == "":
        strmsg = "用户名不能为空\n"
    else:
        r1 = '^[0-9a-zA-Z\-@._]+$'
        if  re.match(r1, username)==None:
            strmsg = strmsg + "用户名只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”"+'\n'


    if mobile == "":
        strmsg = strmsg + "手机号不能为空\n"
    else:
        result = re.search("^1\d{10}$", mobile)  # ^ 表示从什么开始（^1表示从1开始） \d表示0~9之间的数字   {10}表示出现次数为10位$结束
        if result==None:
            strmsg = strmsg + "请您输入正确的手机号\n"
    if password == "":
        strmsg = strmsg + "密码不能为空\n"
    else:
        r1 = '^[0-9a-zA-Z\_]+$'
        if re.match(r1, password) == None:
           strmsg = strmsg + "密码只能是字母加数字，还有下划线\n"
    if  password!=compassword:
        strmsg = strmsg + "密码输入不一致\n"

    if email == "":
        strmsg = strmsg + "邮箱不能为空\n"
    else:
        pattern = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        print( re.match(pattern, email))
        if re.match(pattern, email)==None:
          strmsg = strmsg + "邮箱格式不正确\n"
    if users or strmsg != "":

        if users:
            strmsg = strmsg + f'{mobile}已经注册'
        data = {
            'username': username,
            'password': password,
            'email': email,
            'qq': qq,
            'weChat': wechat,
            'mobile': mobile,
            "info": strmsg
        }
        return render(request, 'regsvr.html', data)
    data={
        'username': username,
        'password': password,
        'email':email,
         'qq':qq,
         'weChat': wechat,
        'mobile':mobile,
        "info" :username+"注册成功"
    }
    Users(username=username,password=password,yhqx=yhqx,email=email,qq=qq,weChat=wechat, mobile=mobile,gender=is_gender).save()

    return render(request, 'regsvr.html', data)
# 登录
def login(request):
    labe = label.objects.all()
    print(request.method)
    username=''
    if request.method == 'GET':
        # 请求页面 有没有cookie 和 session
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
                # return HttpResponseRedirect('/index')
            if  username=='':
                if 'username' in request.session:
                    username= request.session.get('username')
                return HttpResponseRedirect('/index')
        data = {
            "label": labe[:10],
            "labelall": labe,
            'username': '',
            'password': '',
            'error': '',
        }

        return render(request, 'index.html', data)
    if request.method == 'POST':
        # 获取用户输入的账号密码
        mobile=request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 从数据库里对比账号密码
        from index.models import User
        # 判断账号密码是否有问题
        result = Users.objects.filter(mobile=mobile, password=password)
        print(f'mobile{mobile}')
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
        if  username:
            return HttpResponseRedirect('/')

        if result:
            # 账号密码正确记录登录的信息
            print(result.values()[0]['username'])
            username = result.values()[0]['username']
            mobile = result.values()[0]['mobile']
            # 重定向到用户页面，携带username数据
            # Response = HttpResponseRedirect('/index')

            # request.session.
            # Response.set_cookie('username', username, 60 * 60)

            # return Response
        # 返回到个人中心
            strmsg=""
            data = {
                'mobile': mobile,
                'username': username,
                'info': strmsg,
             }
            resp=render(request, 'person.html', data)
            resp.set_cookie('username', username, 60 * 60)
            resp.set_cookie('mobile', mobile, 60 * 60)
            return resp
           # return render(request, 'person.html', Response)
        else:
                    # 当账号密码不正确的时候
            if request.COOKIES.get('username'):

                error ="您已经成功登录"
            else:
                error = "请正确的输入用户名和密码"
                messages.error(request, error)
                return HttpResponseRedirect('/')

                    # data = {
            #     "label": labe[:10],
            #     "labelall": labe,
            #     'username': username,
            #     'password': password,
            #     'error': error,
            # }
            # return render(request, 'index.html', data)

# 个人中心
def  person(request):
    strmsg=""
    data={}
    mobile = request.POST.get('mobile', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    compassword = request.POST.get('compassword', '')
    if username=='':
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
        if 'username' in request.session:
            username=request.session.get('username')
        if 'mobile' in request.COOKIES:
            mobile = request.COOKIES.get('mobile')
        if 'mobile' in request.session:
            mobile = request.session.get('mobile')
    else:
        r1 = '^[0-9a-zA-Z\-@._]+$'
        if re.match(r1, username) == None:
            strmsg = strmsg + "用户名只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”" + '\n'
    if  mobile=='':
        strmsg = strmsg + "手机号不能为空\n"
    if  password=='':
        strmsg = strmsg + "密码不能为空\n"
    else:
        r1 = '^[0-9a-zA-Z\_]+$'
        if re.match(r1, password) == None:
            strmsg = strmsg + "密码只能是字母加数字，还有下划线\n"

    if  password!=compassword:
        strmsg = strmsg + "密码输入不一致\n"
    if  strmsg=='':
        Users.objects.filter(mobile=mobile).update(username=username, password=password)
        strmsg= strmsg + username+ "修改成功\n"
    data = {
        'mobile':mobile,
        'username': username,
        'info': strmsg,
    }
    # resp = HttpResponseRedirect('/regsvr/person')
    resp = render(request, 'person.html', data)
    resp.set_cookie('username', username, 60 * 60)
    resp.set_cookie('mobile', mobile, 60 * 60)
    return resp
    # return render(request, 'person.html', data)
"""注销登录"""
def logout(request):
    """注销登录"""
    from django.http import HttpResponseRedirect
    res = HttpResponseRedirect('/index')  # 重新跳转到登录页面
    # 清除username信息
    if 'username' in request.session:
        del request.session['username']

    if 'username' in request.COOKIES:
        res.delete_cookie('username')
    if 'mobile' in request.session:
        del request.session['mobile']

    if 'mobile' in request.COOKIES:
        res.delete_cookie('mobile')
    return res

def  basetest(request):
    data={}
    return render(request, 'nove_fl.html', data)