from django.shortcuts import render

from index.models import Users
# Create your views here.
def wlyhgl(request):
    mobile = request.POST.get('mobile', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')

    sex = request.POST.get('sex', '')
    is_yhqx = request.POST.get('is_yhqx', '')
    print(f'{mobile}--{is_yhqx}')
    Users(username=username, password=password, yhqx=is_yhqx, email=email, mobile=mobile,
          gender=sex).save()


    return render(request, 'wluser.html')