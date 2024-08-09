import datetime
import random
import re

from django.core import paginator
from django.db.models import Max, Sum,Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import label, Novel, Dynamic, Purchase, Comment, Xsxjpj
from django.contrib import messages
from novel.settings import  *
def index(request):
    labe = label.objects.all()
    novel = Novel.objects.values('bookid').order_by('-fbrq').distinct()[:6]
    list_nove = []
    for  nov in novel:
        bookid=nov['bookid']
        no = Novel.objects.filter(bookid=bookid).values('id')[:1]
        zjs=f'共{len(Novel.objects.filter(bookid=bookid))}章'
        for  ninfo  in  no:
            id=ninfo['id']
            nv = Novel.objects.filter(id=id).values('bookid', 'name', 'singer', 'zjtitle', 'img','type')
            xjsl=0
            for n  in  nv:
                bookid=n['bookid']
                xjsl = Xsxjpj.objects.filter(xsbh=bookid).aggregate(Avg('xjsl'))
                xjpjl=xjsl['xjsl__avg']
                if xjpjl==None:
                    xjpjl=0
                xjsl=f'星级数{xjpjl}'

                dynamic = Dynamic.objects.filter(bookid=n['bookid']).values('lwxh', 'lwkf', 'lwzs', 'lwhc', 'tjsl',
                                                                      'ypsl')[:1]
                gmsl = 0
                xzsl=0
                for  dyn in  dynamic:
                    gmsl=dyn['lwzs']
                    xzsl=dyn['lwkf']

                img = n['img']
                if ' ' in n['zjtitle']:
                         index = n['zjtitle'].index(' ')
                         result = n['zjtitle'][index:]
                else:
                         result=n['zjtitle']
                result1=result.replace('！',' ')
                dis_nov = {}
                dis_nov['bookid'] = n['bookid']
                dis_nov['name'] = n['name']
                dis_nov['singer'] = n['singer']
                dis_nov['zjtitle'] =result1+n['name']
                dis_nov['img'] = img
                dis_nov['zjs'] = zjs
                dis_nov['type'] = n['type']
                dis_nov['xjsl'] = xjsl
                dis_nov['gmsl'] = f'购买{gmsl}次'
                dis_nov['xzsl'] = f'下载{xzsl}次'
            list_nove.append(dis_nov)

    #根据小说的星级别

    list_xsxj=[]
    xsxjpj = Xsxjpj.objects.values('xsbh').annotate(Avg('xjsl')).order_by('-xjsl__avg')[:6]
    for  xsxj  in  xsxjpj:
        dis_xsxj  = {}
        bookid=xsxj['xsbh']
        xjsl = f'星级数{round(xsxj["xjsl__avg"],2)}'
        print(f'星级数{xjsl}')
        novel = Novel.objects.filter(bookid=bookid)
        zjs = f'共{len(novel)}章'
        for   nov in novel:
              dynamxj = Dynamic.objects.filter(bookid=bookid).values('lwxh', 'lwkf', 'lwzs', 'lwhc', 'tjsl',
                                                                          'ypsl')[:1]
              gmsl = 0
              xzsl = 0
              for dyn in dynamxj:
                  gmsl = dyn['lwzs']
                  xzsl = dyn['lwkf']
              dis_xsxj['bookid'] = nov.bookid
              dis_xsxj['name'] = nov.name
              dis_xsxj['singer'] = nov.singer
              dis_xsxj['type'] = nov.type
              dis_xsxj['xjsl'] = xjsl
              dis_xsxj['gmsl'] = f'购买{gmsl}次'
              dis_xsxj['xzsl'] =  f'下载{xzsl}次'
              dis_xsxj['zjs'] = zjs
              dis_xsxj['img'] = nov.img
        list_xsxj.append(dis_xsxj)
        # print(f'星级{len(list_xsxj)}')
    #搜索次数
    list_sscs = []
    dynamss=Dynamic.objects.all().order_by('-tjsl')[:6]
    for  dyna  in  dynamss:

        bookid = dyna.bookid

        novel = Novel.objects.filter(bookid=bookid)[:1]
        zjs = f'共{len(novel)}章'
        xjsl = Xsxjpj.objects.filter(xsbh=bookid).aggregate(Avg('xjsl'))
        xjpjl = xjsl['xjsl__avg']
        if xjpjl == None:
            xjpjl = 0
        xjsl = f'星级数{ round(xjpjl,2)}'
        dynamss = Dynamic.objects.filter(bookid=bookid).values('lwxh', 'lwkf', 'lwzs', 'lwhc', 'tjsl')

        gmsl=0
        xzsl = 0
        for dyn in dynamss:
            gmsl = dyn['lwzs']
            xzsl = dyn['lwkf']
        for nov in novel:
            dis_sssl= {}
            dis_sssl['bookid'] = nov.bookid
            dis_sssl['name'] = nov.name
            print(f'搜索{nov.bookid}')
            dis_sssl['singer'] = nov.singer
            dis_sssl['type'] = nov.type
            dis_sssl['xjsl'] = xjsl
            dis_sssl['gmsl'] = f'购买{gmsl}次'
            dis_sssl['xzsl'] = f'下载{xzsl}次'
            dis_sssl['zjs'] = zjs
            dis_sssl['img'] = nov.img
        list_sscs.append(dis_sssl)

    # 购买次数
    list_gmcs = []
    dynamgm = Dynamic.objects.all().order_by('-lwzs')[:6]
    for dyna in dynamgm:

        bookid = dyna.bookid
        novel = Novel.objects.filter(bookid=bookid)[:1]
        zjs = f'共{len(novel)}章'
        xjsl = Xsxjpj.objects.filter(xsbh=bookid).aggregate(Avg('xjsl'))
        xjpjl = xjsl['xjsl__avg']
        if xjpjl == None:
            xjpjl = 0
        xjsl = f'星级数{round(xjpjl,2)}'
        gmsl = dyna.lwzs
        xzsl = dyna.lwkf
        print(f'购买2{gmsl}次')
        for nov in novel:
            dis_gmcs = {}
            dis_gmcs['bookid'] = nov.bookid
            dis_gmcs['name'] = nov.name
            dis_gmcs['singer'] = nov.singer
            dis_gmcs['type'] = nov.type
            dis_gmcs['xjsl'] = xjsl
            dis_gmcs['gmsl'] = f'购买{gmsl}次'

            dis_gmcs['xzsl'] = f'下载{xzsl}次'
            dis_gmcs['zjs'] = zjs
            dis_gmcs['img'] = nov.img
        list_gmcs.append(dis_gmcs)
    print(len(list_gmcs))

    username=""
    if 'username' in request.COOKIES:
        username=request.COOKIES.get('username')

    if 'username' in request.session:
        username=request.session.get('username')
    if  username:
        error=username+'已登录'
    else:
        error = '请正确的输入用户名和密码'
    listrm=[]
    for li in list_xsxj[0:5]:
        dis = {}
        dis['lbname'] = li['name']
        dis['bookid'] = li['bookid']
        listrm.append(dis)

    dynamic=Dynamic.objects.all().values("bookid").annotate(lwzs=Max("lwzs")).order_by('lwzs').last()
    # print(dynamic)
    bookid = dynamic['bookid']
    nv = Novel.objects.filter(bookid=bookid).values('bookid', 'name').distinct()[:1]

    for n  in  nv:
        dis = {}
        dis['lbname']=n['name']
        dis['bookid'] = n['bookid']
    listrm.append(dis)

    print(f'listrm{listrm}')



    data={
        "MEDIA_URL": MEDIA_URL,
        "label": labe[:11],
        "labelall": labe[:12],
        "error":error,
        "list_nove":list_nove,
        "list_ydzx": list_nove[:4],
        "listrm":listrm,
        "list_xsxj":list_xsxj,
        "list_sscs":list_sscs,
        "list_gmcs":list_gmcs,
        "username": username

    }
    # print(MEDIA_URL)
    return render(request, 'index.html', data)
def nove_fl(request,label_id,page):
    user=''
    mobile=''
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
    if 'mobile' in request.COOKIES:
        mobile = request.COOKIES.get('mobile')
    if mobile == "":
        if 'mobile' in request.session:
            mobile = request.session.get('mobile')

    list_nove=[]
    data={}
    if  label_id==0:
        labe = label.objects.all()
        novel = Novel.objects.values('bookid').distinct()
    else:
        # print(label_id)
        labe = label.objects.filter(id=label_id)
        novel = Novel.objects.filter(label_id=label_id).values('bookid').distinct()
        # print(len(novel))
    pages = paginator.Paginator(novel, 18)
    novel = pages.get_page(page)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]
    # page=2
    page_index = total_list.index(page)

    # data['totle_page'] = total_list
    if page >= 3:
        total_list = total_list[total_list[page_index] - 3:total_list[page_index] + 2]
    else:
        total_list = total_list[:total_list[page_index] + 2]


    for nov in novel:
        is_hy=''
        bookid = nov['bookid']
        no = Novel.objects.filter(bookid=bookid).values('id')[:1]


        zjs = f'共{len(Novel.objects.filter(bookid=bookid))}章'
        for ninfo in no:
            id = ninfo['id']
            nv = Novel.objects.filter(id=id).values('bookid', 'name', 'singer', 'zjtitle', 'img', 'type','iswj','label_id','fbrq')
            for n in nv:
                img = n['img']
                if ' ' in n['zjtitle']:
                    index = n['zjtitle'].index(' ')
                    result = n['zjtitle'][index:]
                else:
                    result = n['zjtitle']
                dynamic= Dynamic.objects.filter(bookid=n['bookid']).values('lwxh','lwkf','lwzs','lwhc','tjsl','ypsl')[:1]

                xzsl=0
                gmsl=0
                ydsl=0
                if  dynamic:
                    for dynam in  dynamic:
                         xzsl=dynam['lwkf']
                         gmsl = dynam['lwzs']
                         ydsl = dynam['lwxh']
                         print(dynam)

                purchase = Purchase.objects.filter(xsbh=bookid, userid=mobile)
                if purchase:
                    is_hy = 'Y'
                dis_nov = {}
                dis_nov['bookid'] = n['bookid']
                dis_nov['name'] = n['name']
                dis_nov['singer'] = n['singer']
                dis_nov['img'] = img
                dis_nov['zjs'] = zjs
                dis_nov['type'] = n['type']
                dis_nov['fbsj'] = n['fbrq']
                dis_nov['iswj'] = n['iswj']

                dis_nov['xzsl'] = f'下载{xzsl}次'
                dis_nov['gmsl'] =f'购买{gmsl}次'
                dis_nov['ydsl'] = ydsl
                dis_nov['label_id'] = label_id
                dis_nov['is_hy'] = is_hy

                list_nove.append(dis_nov)

    # print(list_nove)
    # list_nove = sorted(list_nove, key=lambda x: -x['gmsl'])
    list_nove=sorted(list_nove, key=lambda x: x['gmsl'], reverse=True)
    # list_nove = sorted(list_nove, key=lambda x: (x['gmsl']))
    # list_nove=list_nove.sort(reverse=True)
    # print(list_nove)
    data = {
        "MEDIA_URL": MEDIA_URL,
        "label": labe,
        "list_nove":list_nove,
        "totle_page":total_list,
        "label_id":label_id
    }
    # print(labe)
    return render(request, 'nove_fl.html', data)
def nove_yued(request,bookid,flage):
    # 判断是否登录
    info=""
    user=""
    mobile=''
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if  user=="":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')
    print(user)
    if  user=='':
        # messages.error(request,'请您先登录')
        return HttpResponseRedirect('/')
        # return HttpResponseRedirect('/flxx/0/1')
    if  flage=='sy': #首页跳转
        purchase = Purchase.objects.filter(userid=mobile, xsbh=bookid)
        if purchase:
            flage='yd'
        else:
            flage='gm'

    if  flage=="yd":
        purchase=Purchase.objects.filter(userid=mobile,xsbh=bookid)
        list_nove=[]
        if purchase: # 存在 跳转阅读界面
            novel = Novel.objects.filter(bookid=bookid).values('id','zjtitle').order_by('id')[:20]
            res = '背景介绍：'
            for ninfo in novel:
                id = ninfo['id']
                nv = Novel.objects.filter(id=id).values('bookid', 'name', 'singer', 'zjtitle', 'img', 'type', 'fbrq')
                for n in nv:
                    img = n['img']
                    if ' ' in n['zjtitle']:
                        index = n['zjtitle'].index(' ')
                        result = n['zjtitle'][index:]
                    else:
                        result = n['zjtitle']
                    result = result.replace('！', ' ')
                    res = res + result
                    dis_nov = {}
                    dis_nov['bookid'] = n['bookid']
                    dis_nov['name'] = n['name']
                    dis_nov['singer'] = '作者:' + n['singer']
                    dis_nov['zjtitle'] = res
                    dis_nov['img'] = img
                    dis_nov['fbrq'] = '发布日期:' + n['fbrq']
                    name=n['name']

            list_nove.append(dis_nov)
            comment = Comment.objects.filter(userid=mobile)
            pages = paginator.Paginator(comment, 16)
            comment = pages.get_page(1)
            totle_page = pages.num_pages
            total_list = [i for i in range(1, totle_page + 1)]

            dynamic = Dynamic.objects.filter(bookid=bookid)
            if dynamic:
                for dynam in dynamic:
                    lwxh = dynam.lwxh + 1
                    print(lwxh)
                    Dynamic.objects.filter(bookid=bookid).update(lwxh=lwxh)
            else:
                Dynamic(lwxh=1, lwkf=1, lwzs=0, lwhc=0, tjsl=0, ypsl=0, bookid=bookid).save()

            print('可以阅读')
            data={
                'comment': comment,
                'totle_page': total_list,
                "MEDIA_URL": MEDIA_URL,
                'list_nove': list_nove,
                'novel':novel,
                 'name':name,
                 'bookid':bookid
            }
            return render(request, 'noveyued.html', data)
        else:
            messages.error(request, '请您购买小说后在阅读')
            return HttpResponseRedirect('/flxx/0/1')
    # print(flage)
    if  flage=='gm':
        list_nove=[]
        novel = Novel.objects.filter(bookid=bookid).values('id')
        zjs = f'共{len(Novel.objects.filter(bookid=bookid))}章'
        print(novel)
        res = '背景介绍：'
        for  ninfo  in novel:
            id = ninfo['id']

            nv = Novel.objects.filter(id=id).values('bookid', 'name', 'singer', 'zjtitle', 'img', 'type','fbrq')

            for n in nv:
                img = n['img']
                if ' ' in n['zjtitle']:
                    index = n['zjtitle'].index(' ')
                    result = n['zjtitle'][index:]
                else:
                    result = n['zjtitle']

                result=result.replace('！', ' ')
                # print(f'result{result}')
                # print(f'res1{res}')
                res =res+result
                # print(f'res{res}')
                dis_nov = {}
                dis_nov['bookid'] = n['bookid']
                dis_nov['name'] = n['name']
                dis_nov['singer'] ='作者:'+ n['singer']
                dis_nov['zjtitle'] = res
                dis_nov['img'] = img
                dis_nov['zjs'] = zjs
                dis_nov['type'] = n['type']
                dis_nov['fbrq'] = '发布日期:'+n['fbrq']
                dis_nov['user'] = '登录人:' + user

        list_nove.append(dis_nov)

        print(list_nove[-1])
        data={
            "MEDIA_URL": MEDIA_URL,
            'list_nove':list_nove,

        }
        return render(request, 'purchase.html', data)

