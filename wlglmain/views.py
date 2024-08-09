from django.shortcuts import render
from index.models import wlglqx
from django.contrib import messages
from novel.settings import  *
# Create your views here.
def wlglmain(request):
    print('wlmain')
    #
    wlgl= wlglqx.objects.filter(LP04='Y',LP03='1'  ).values('LP01', 'LP02','LP03', 'LP04','LP05').order_by("LP05")
    yjlt= list(wlgl.values())

    wlglgn = wlglqx.objects.filter(LP04='Y', LP03='2').values('LP01', 'LP02', 'LP03', 'LP04', 'LP05','LP06').order_by("LP05")
    ejlt = list(wlglgn.values())
    disgn = {}
    ltej=[]
    ltyj = []
    for  yj  in yjlt:
        disgn = {}
        ltej=[]
        disgn['LP02'] = yj['LP02']

        for  ej in  ejlt:


            if  yj['LP01'] ==  str(ej['LP01'])[:2]:
                # print(disgn['LP02'] )
                ltgn = {}
                ltgn['LP02'] = ej['LP02']
                ltgn['LP06'] = ej['LP06']
                ltej.append(ltgn)
            disgn['lt']=ltej
        # print(disgn)
        ltyj.append(disgn)
        print(ltyj)

    #
    #
    # print(ltyj)

    # disyj={}
    # disej={}
    # ltyj = []
    # ltej = []
    # for  li  in  lit:
    #     if li['LP03']=='1':
    #         ltej=[]
    #         # print(li['LP02'])
    #         disej['LP02']=li['LP02']
    #     if li['LP03']=='2':
    #         # print(li['LP02'])
    #         ltyj={}
    #         ltyj['LP02'] = li['LP02']
    #         ltej.append(ltyj)
    #         disej['lt'] = ltej
    #     if len(ltej)==0:
    #         continue

        # print(disej)
        # disej['lt'] = ltej
        #     ltyj.append(disej)
        # print(disej)
        # ltyj.append(disyj)
    # print(ltyj)
    #
    # my_wlgl=[{'LP02':'基础信息','lt':[{"LP02":"员工信息"},{"LP02":"权限设置"}]},{'LP02':'物流轨迹','lt':[{"LP02":"轨迹设置"},{"LP02":"轨迹修改"}]}]
    # print(my_wlgl)
    return render(request, 'wlmain.html',{
        'my_wlgl': ltyj})