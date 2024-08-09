import datetime

from django.core import paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import Dynamic, Novel, Xsxjpj
from novel.settings import MEDIA_URL


def ranking(request,page):
    list_nove=[]
    dynamic=Dynamic.objects.all().order_by('-lwzs','-lwkf')
    pages = paginator.Paginator(dynamic, 8)
    dynamic = pages.get_page(page)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]

    for  dyn in   dynamic:
        bookid=dyn.bookid
        novel=Novel.objects.filter(bookid=bookid).distinct()[:1]
        for  n in  novel:
            dis_nov = {}
            dis_nov['bookid'] = n.bookid
            dis_nov['name'] = n.name
            dis_nov['singer'] = n.singer
            dis_nov['img'] = n.img
            dis_nov['lwzs'] = dyn.lwzs
            dis_nov['fbrq'] = n.fbrq
            dis_nov['lwkf'] = dyn.lwkf
        list_nove.append(dis_nov)
    data={
        'list_nove':list_nove,
        "MEDIA_URL": MEDIA_URL,
        'totle_page': total_list,

    }

    return render(request, 'xspm.html', data)
def  xsxjpj(request,bookid,xjpj):
     data={}
     now = datetime.datetime.now()
     xjrq=now.strftime("%Y-%m-%d %H:%M:%S")
     print(f'xjpj{xjpj}')
     user = ""
     mobile = ''
     if 'username' in request.COOKIES:
         user = request.COOKIES.get('username')
         mobile = request.COOKIES.get('mobile')
     if user == "":
         if 'username' in request.session:
             user = request.session.get('username')
             mobile = request.session.get('mobile')
     print(user)
     xsxjpj=Xsxjpj.objects.filter(userid=mobile,xsbh=bookid)
     if  xsxjpj:
             Xsxjpj.objects.filter(userid=mobile,xsbh=bookid).update(xjsl=xjpj)
     else:
         Xsxjpj(userid=mobile, username=user,xsbh=bookid,  xjsl=xjpj,pjrq=xjrq).save()

     return HttpResponseRedirect(f"/nove_yued/{bookid}/yd")
