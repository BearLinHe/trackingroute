from django.core import paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from index.models import Novel, label, Purchase, Dynamic
from novel.settings import MEDIA_URL


def search(request):
    search_text = request.POST.get('search_text', '')
    user = ''
    mobile = ''
    label_id=0
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

    list_nove = []
    data = {}

    labe = label.objects.all()


    # novel = Novel.objects.values('bookid').distinct()
    novel = Novel.objects.filter(Q(name__icontains=search_text) | Q(singer__icontains=search_text)).values("bookid").distinct()
    print(novel)
    pages = paginator.Paginator(novel, 18)
    novel = pages.get_page(1)
    totle_page = pages.num_pages
    total_list = [i for i in range(1, totle_page + 1)]
    # page=2
    page_index = total_list.index(1)
    for nov in novel[:1]:
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
                print(dynamic)
                print(n['bookid'])
                if  dynamic:
                    for dynam in  dynamic:
                         xzsl=dynam['lwkf']
                         gmsl = dynam['lwzs']
                         ydsl = dynam['lwxh']
                         tjsl =dynam['tjsl'] + 1
                         Dynamic.objects.filter(bookid=n['bookid']).update(tjsl=tjsl)
                else:
                    Dynamic(lwxh=0, lwkf=0, lwzs=0, lwhc=0, tjsl=1, ypsl=0, bookid=bookid).save()


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


    data = {
        "MEDIA_URL": MEDIA_URL,
        "label": labe,
        "list_nove":list_nove,
        "totle_page":total_list,
        "label_id":label_id
    }



    return render(request, 'nove_fl.html', data)
