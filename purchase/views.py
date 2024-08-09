import datetime
import os
import re
from urllib import parse

from django.contrib import messages
from django.core import paginator
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.encoding import escape_uri_path

from index.models import Purchase, Novel, Comment, Dynamic, Read
from novel.settings import MEDIA_URL
from django.db.models import Q



def purchase(request,bookid):
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')

    novel = Novel.objects.filter(bookid=bookid).values('name').distinct()[:1]
    print(bookid)
    now = datetime.datetime.now()
    goum_date = now.strftime("%Y-%m-%d")
    for no in novel:
        name=no['name']
        Purchase.objects.filter(userid=mobile,xsbh=bookid).delete()
        Purchase(userid=mobile, username=user, xsbh=bookid, name=name, sfgm='Y',gmrq=goum_date).save()

        dynamic = Dynamic.objects.filter(bookid=bookid)

        print(bookid)
        if dynamic:
            for dynam in dynamic:
                lwzs = dynam.lwzs + 1
                print(f'购买{lwzs}---{dynam.lwzs}')
                Dynamic.objects.filter(bookid=bookid).update(lwzs=lwzs)
        else:
            Dynamic(lwxh=0, lwkf=0, lwzs=1, lwhc=0, tjsl=0, ypsl=0, bookid=bookid).save()


    messages.error(request, '购买成功')

    purchase = Purchase.objects.filter(userid=mobile, xsbh=bookid)
    list_nove = []
    if purchase:  # 存在 跳转阅读界面
        novel = Novel.objects.filter(bookid=bookid).values('id', 'zjtitle').order_by('id')[:20]
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
                name = n['name']

        list_nove.append(dis_nov)
        comment = Comment.objects.filter(userid=mobile)
        pages = paginator.Paginator(comment, 17)
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
        data = {
            'comment': comment,
            'totle_page': total_list,
            "MEDIA_URL": MEDIA_URL,
            'list_nove': list_nove,
            'novel': novel,
            'name': name,
            'bookid': bookid
        }
        return render(request, 'noveyued.html', data)



    # comment(request,bookid,1)

    return HttpResponseRedirect(f"/yued/{bookid}/{'gm'}")

def comment(request,bookid,page):
    list_nove=[]
    user=''
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')
    # 如果未登录需要跳转到登录页面
    if user=='':
        return HttpResponseRedirect("/")

    novel = Novel.objects.filter(bookid=bookid).values('name').distinct()
    for no in novel:
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        name=no['name']
        comment_text = request.POST.get('comment', '')
        if comment_text:
           Comment(userid=mobile, username=user, bookid=bookid, name=name, plrq=formatted_date,content=comment_text).save()
        comment = Comment.objects.filter(userid=mobile)
        pages = paginator.Paginator(comment, 16)
        comment = pages.get_page(page)
        totle_page = pages.num_pages

        total_list = [i for i in range(1, totle_page + 1)]
        page_index = total_list.index(page)
        if page >= 3:
            total_list = total_list[total_list[page_index] - 3:total_list[page_index] + 2]
        else:
            total_list = total_list[:total_list[page_index] + 2]

        novel = Novel.objects.filter(bookid=bookid).values('id', 'zjtitle').order_by('id')[:20]
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
        print(name)
        data = {
                'comment': comment,
                'totle_page': total_list,
                "MEDIA_URL": MEDIA_URL,
                'list_nove': list_nove,
                'novel': novel,
                 'name':name,
                 'bookid':bookid
                }
        return render(request, 'noveyued.html', data)
def download(request,bookid):
    # 记录下载次数

     novel=Novel.objects.filter(bookid=bookid).distinct()[:1]
     # song.download=song.download+1
     # song.save()
     # novel = novel.objects.get(bookid=bookid)
     for nov in novel:
         dynamic=Dynamic.objects.filter(bookid=bookid)[:1]
         # novel = Novel.objects.filter(bookid=bookid).values('id').distinct()[:1]
         print(bookid)
         if  dynamic:
             for  dynam in dynamic:
                lwkf=dynam.lwkf+1
                print(lwkf)
                Dynamic.objects.filter(bookid=bookid).update(lwkf=lwkf)
         else:
             Dynamic(lwxh=0, lwkf=1, lwzs=0, lwhc=0, tjsl=0, ypsl=0, bookid=bookid).save()

         file=parse.unquote(nov.file.url[1::])#去除前面的 /
         file =os.path.split(file)[0]+'.zip'
         fname=nov.name+'.zip'
         response = StreamingHttpResponse(open(file, "rb"))
         # response = StreamingHttpResponse(file_iterator(file))
         response['Content-Type'] = 'application/octet-stream'
         response["Content-Disposition"] = "attachment; filename*=UTF-8\'\'{}".format(escape_uri_path(fname))
         return response


def novread(request,id,page):
    # 阅读也需要判断权限
    print(f'ida{id}')
    user=""
    mobile=""
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')

    if  user == "":
        # messages.error(request,  '请您登录在阅读')
        # return HttpResponseRedirect('/flxx/0/1')
        return HttpResponseRedirect('')

    list_nove = []
    novel=Novel.objects.filter(id=id).values('name','zjnum','zjtitle','file','bookid','singer','type')

    for  no in  novel:

        bookid=no['bookid']
        name = no['name']
        title = no['zjtitle']
        zjnum=no['zjnum']
        singer=no['singer']
        type = no['type']
        print(f'id1{title}')
    purchase = Purchase.objects.filter(userid=mobile, xsbh=bookid)
    if  len(purchase)==0:
        messages.error(request, '请您购买后在阅读')
        return HttpResponseRedirect('/flxx/0/1')

        # return HttpResponseRedirect(f'/yued/{bookid}/1')
    print(f'{id}---{bookid}')
    zszj=len(Novel.objects.filter(bookid=bookid))

    startxh=id - 5
    endxh =id+5
    # print(startxh)
    # print(endxh)
    q1 = Q(id__gt=startxh)
    q2 = Q(id__lt= endxh)
    q3 = Q(bookid = bookid)
    novel= Novel.objects.filter(q1 & q2 & q3).order_by('id')
    # novel = Novel.objects.filter(idrange=[startxh,endxh] ,bookid=bookid).order_by(id)

    for  n  in  novel:
        dis_nov = {}
        zjtitle=n.zjtitle.split(' ',1)[0]
        # print(zjtitle)
        dis_nov['bookid'] = n.bookid
        dis_nov['name'] = n.name
        dis_nov['id'] = n.id
        dis_nov['zjnum'] =n.zjnum
        dis_nov['zjtitle'] = zjtitle
        dis_nov['title'] = n.zjtitle
        dis_nov['file'] = n.file
        list_nove.append(dis_nov)
    # filenames = os.listdir(dir) # 作者目录下的作品列表
    content=''
    for filename  in  list_nove:

         # file=filename ['file']

         file = parse.unquote(filename ['file'].url[1::])
         # print(os.path.exists(file))
         # print(file)
         with open(file, 'r',encoding='UTF-8') as f:
            data = f.readline()
            # data.replace("\n\t\t\t\t\t\t\t",' ').replace("\t",' ')
            # data=re.sub('\t', ' ', data)
            # data = re.sub('\n', ' ', data)
            data=re.sub(r'\\t|\\n', '', data)
            data=data.replace('[','').replace('""','')
            data=data.rstrip()
            content+=data
            # content+= [" ", " "]
            # print(data)
            f.close()

            # content += [line for line in open(file, 'r', encoding='UTF-8')]  # 收集作品中的所有行
    #      print("open = ", open( file, 'r', encoding='UTF-8'))
    #      content += [" ", " "]  # 加两个空行
    # print("content = ", content)

    content = content.strip('').strip('[]').split(',')
    content=''.join(content)
    content = content.replace(' ', '')
    content = content.replace(' ', '')
    content = ''.join(content.split(' '))
    pattern  = re.compile(r'\s+');

    content=re.sub(pattern , '', content);
    words = content.rstrip()

    pages = paginator.Paginator(words, 2000)
    content = pages.get_page(page)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]
    ls_str=''

    read = Read.objects.filter(userid=mobile, xsbh=bookid)
    if page == 1:
        if read.count() == 0:
            Read(userid=mobile, username=user, xsbh=bookid, name=name, ydzj=1, ydid=id, xszj=zszj, sfwj='未完结',
                 type=type).save()
        else:
            for rea in read:
                ydzj = int(rea.ydzj) + 1
                # print(f'ydzj{ydzj}--{bookid}')
                sfwj = '未完结'
                if ydzj >= int(rea.xszj):
                    sfwj = '已完结'
                    ydzj= '已阅读'
                Read.objects.filter(userid=mobile, xsbh=bookid).update(ydzj=ydzj, ydid=id, sfwj=sfwj)
    if page>1:
        for s in  content:
            ls_str=ls_str+s
        for   li  in  list_nove:
            # print(li)

            if li['zjtitle']  in   ls_str:
                id = li['id']
                # print(li['id'])
                if page!=1:
                    title=li['title']
                    zjnum=li['zjnum']

                else:
                    # id = li['id']
                    read = Read.objects.filter(userid=mobile, xsbh=bookid)
                    if read.count() == 0:
                        Read(userid=mobile, username=user, xsbh=bookid, name=name, ydzj=1, ydid=id, xszj=zszj, sfwj='未完结',
                             type=type).save()
                    else:

                        for rea in read:
                            ydzj = int(rea.ydzj) + 1
                            # print(f'ydzj{ydzj}--{bookid}--{id}')
                            # print(f'idzhang{id}')
                            sfwj = '未完结'
                            if ydzj == int(rea.xszj):
                                sfwj = '已完结'
                            Read.objects.filter(userid=mobile, xsbh=bookid).update(ydzj=ydzj, ydid=id, sfwj=sfwj)    #

    # print(f'id2{title}')
    data={
        'list_nove':list_nove,
        'name':name,
        'title':title,
        'zjnum':zjnum,
        'singer':singer,
        'content':content,
         'id':id,
        'totle_page': total_list,
    }
    return render(request, 'read.html', data)
# 消息通知
def  information(request,page,plpage):
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')
    if user=='':
        return HttpResponseRedirect("/")

    purchase= Purchase.objects.filter(userid=mobile)

    pages = paginator.Paginator(purchase, 6)
    purchase = pages.get_page(page)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]

    list_nove=[]
    for  pur in purchase:
        bookid=pur.xsbh
        readinfo=Read.objects.filter(userid=mobile,xsbh=bookid)
        iswj='未完结'
        if  readinfo:
            for  read in  readinfo:
                if  read.ydzj!=read.xszj:
                    iswj='未完结'
                else:
                    iswj = '已完结'
        dis_nov = {}
        novel = Novel.objects.filter(bookid=bookid).values('id', 'zjtitle').order_by('id')
        zjs = f'共{len(Novel.objects.filter(bookid=bookid))}章'
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
                result= re.sub(r'\d+', '', result)

                res = res + result

                dis_nov['bookid'] = n['bookid']
                dis_nov['name'] = n['name']
                dis_nov['singer'] = '作者:' + n['singer']
                dis_nov['zjtitle'] = res
                dis_nov['img'] = img
                dis_nov['fbrq'] = '发布日期:' + n['fbrq']
                dis_nov['zjs'] = zjs
                dis_nov['type'] = n['type']
                dis_nov['gmrq'] = '购买日期:'+pur.gmrq
                dis_nov['iswj'] = iswj

        list_nove.append(dis_nov)
    list_pl=[]
    comment = Comment.objects.filter(username='999')
    for  li  in  list_nove:        #
        singer=li['singer'].split(':')[1]
        # singer='zhangzong'
        print(f'singer{bookid}')
        comment = Comment.objects.filter(username=singer)

        if  comment:
            for com  in comment:
                dis_com={}
                dis_com['plrq']=com.plrq
                dis_com['username'] = com.username
                dis_com['content'] = com.content
                dis_com['name'] = com.name
                list_pl.append(dis_com)
                print(f'com{ com.name}')
        # comment =Comment.objects.all()
    pages = paginator.Paginator(list_pl, 8)
    list_pl = pages.get_page(1)
    #
    pl_page = pages.num_pages
    totalpl_list = [i for i in range(1, pl_page + 1)]

    data={
        "comment":comment,
        "MEDIA_URL": MEDIA_URL,
        "list_nove":list_nove,
        'totle_page': total_list,
        'totalpl_list':totalpl_list,
        "list_pl" :list_pl
    }

    # print(data)
    return render(request,'information.html',data)

def mynove(request,page):
    downlist = request.POST.get('downlist', '')
    downlis2 = request.POST.get('downlis2', '')

    user=''
    mobile=''
    if 'username' in request.COOKIES:
        user = request.COOKIES.get('username')
        mobile = request.COOKIES.get('mobile')
    if user == "":
        if 'username' in request.session:
            user = request.session.get('username')
            mobile = request.session.get('mobile')
    if user == "":
        return HttpResponseRedirect('/')


    purchase = Purchase.objects.filter(userid=mobile).order_by('id')
    gyxs = f'VIP【{user}】共{len(purchase)}本小说'


    dis_type =[]
    list_nove=[]
    pages = paginator.Paginator(purchase, 6)
    purchase = pages.get_page(page)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]
    ydid=''
    print(purchase)
    if  purchase:
        for   pur in  purchase:

            bookid=pur.xsbh
            readinfo = Read.objects.filter(userid=mobile, xsbh=bookid)
            iswj = '未完结'
            ydzj = f'已读0章'
            ydzt='未阅读'

            if readinfo:
                for read in readinfo:

                    if read.ydzj != read.xszj:
                        iswj = '未完结'
                        ydzt='正在阅读'

                    else:
                        iswj = '已完结'
                        ydzt = '已阅读'
                    ydid=read.ydid
                    print(f'阅读id{ydid}')
                    ydzj = f'已读{read.ydzj}章'

            dis_nov = {}

            novel = Novel.objects.filter(bookid=bookid).values('id', 'zjtitle').order_by('id')
            zjs = f'共{len(Novel.objects.filter(bookid=bookid))}章'
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
                    result = re.sub(r'\d+', '', result)
                    res = res + result
                    dis_nov['bookid'] = n['bookid']
                    dis_nov['name'] = n['name']
                    dis_nov['singer'] = '作者:' + n['singer']
                    dis_nov['zjtitle'] = res
                    dis_nov['img'] = img
                    dis_nov['fbrq'] = '发布:' + n['fbrq']
                    dis_nov['zjs'] = zjs
                    dis_nov['type'] = n['type']
                    dis_nov['gmrq'] = '购买日期:' + pur.gmrq
                    dis_nov['iswj'] = iswj
                    dis_nov['ydzj'] = ydzj
                    dis_nov['ydzt'] = ydzt
                    if ydid:
                       dis_nov['ydid'] = ydid
                    else:
                        dis_nov['ydid'] = id
                    dis_nov['id'] = id
            dis_type.append(dis_nov)
            # list_nove.append(dis_nov)
            # dis_type=list_nove


            xstype='全部'
            ydzt=downlist
            xstype=downlis2

            if  ydzt=='':
                ydzt = '全部'
            if xstype == '':
                xstype = '全部'
            if   ydzt == '全部'   and   xstype=='全部':
                list_nove.append(dis_nov)
            if ydzt != '全部' and   xstype!='全部':

               print(dis_nov['ydzt'])
               if  ydzt==dis_nov['ydzt']  or   ydzt==dis_nov['iswj']  or   xstype==dis_nov['type']:
                   list_nove.append(dis_nov)
            if  ydzt != '全部'  and xstype=='全部':
                if ydzt == dis_nov['ydzt'] or ydzt == dis_nov['iswj']:
                    list_nove.append(dis_nov)
            if  ydzt=='全部'  and  xstype!='全部':
                if  xstype==dis_nov['type']:
                    list_nove.append(dis_nov)


        data = {
            'list_nove':list_nove,
            'dis_type':dis_type,
            'total_list': total_list,
            "MEDIA_URL": MEDIA_URL,
             'gyxs':gyxs,

        }
        # print(data)



    return render(request, 'mynove.html', data)
# def ranking(request,page):
#     list_nove=[]
#     dynamic=Dynamic.objects.all().order_by('-lwzs','-lwkf')
#     pages = paginator.Paginator(dynamic, 8)
#     dynamic = pages.get_page(1)
#     totle_page = pages.num_pages
#     total_list = [i for i in range(1, totle_page + 1)]
#
#     for  dyn in   dynamic:
#         bookid=dyn.bookid
#         novel=Novel.objects.filter(bookid=bookid).distinct()[:1]
#         for  n in  novel:
#             dis_nov = {}
#             dis_nov['bookid'] = n.bookid
#             dis_nov['name'] = n.name
#             dis_nov['singer'] = n.singer
#             dis_nov['img'] = n.img
#             dis_nov['lwzs'] = dyn.lwzs
#             dis_nov['fbrq'] = n.fbrq
#             dis_nov['lwkf'] = dyn.lwkf
#         list_nove.append(dis_nov)
#     data={
#         'list_nove':list_nove,
#         "MEDIA_URL": MEDIA_URL,
#         'totle_page': total_list,
#
#     }
#
#     return render(request, 'xspm.html', data)