import dateutil
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import uuid

# Create your views here.
from index.models import Logisticstrajectory, Transport
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from  wlgjsc.工具信息 import Tools
from  wlgjsc.美国物流距离分割算法 import Get_wlinxfo;
def create_uuid():
    return uuid.uuid4().hex
def convert_date_en(date_str):
    # 解析输入的日期时间字符串
    dt_obj = dateutil.parser.parse(date_str)
    english_date = dt_obj.strftime('%d %B, %Y at %H:%M')

    # 使用strftime来格式化输出为 mm/dd pm/am 格式
    return english_date
def wlgjgx(request):
    print('wlg_tree1')

    return render(request, 'wlxg.html')

def wlg_tree(request):
    print('wlg_tree')
    now = datetime.now()
    before_15_days = now - timedelta(days=15)
    before_15_days=f"{before_15_days.strftime('%Y-%m-%d ')}00:00:00"
    # 获取后15天的日期
    after_15_days = now + timedelta(days=15)
    after_15_days=f"{after_15_days.strftime('%Y-%m-%d ')}23:59:59"
    print(after_15_days)





    transport=Transport.objects.filter(Q(TP14__gt=before_15_days) & Q(TP14__lt=after_15_days)).values('TP01','TP02','TP03','TP04','TP05','TP06','TP07','TP08','TP09','TP14','TP15','TP16')
    # print(f'transport--{transport}')
    unique_tran=transport.values_list('TP16',flat=True).distinct()


    my_tran = list(transport.values())
    unique_list=list(unique_tran)

    disrq_list = []
    dishwbh_list=[]
    data=[]
    for index, value  in  enumerate(unique_list):
        disyf={}
        disrq = {}
        dishwbh = {}
        disrq_list=[]
        disyf['title']=value
        disyf['id'] = index
        disyf['ismw'] = '0'
        unique_yf = transport.filter(TP16=value).values_list('TP15',flat=True).distinct()
        unique_yflist = list(unique_yf)

        # print(f"unique_yflist--{unique_yflist}")
        for inde, value in enumerate(unique_yflist):
            disrq={}
            dishwbh_list=[]
            disrq['title']=value
            disyf['ismw'] = '0'
            disrq['id'] = inde+index
            unique_data=transport.filter(TP15=value)
            unique_dalist= list(unique_data)
            # print(f'value--{value} {len(unique_dalist)}')
    #         # print( f'unique_dalist--{unique_dalist}')
    # #         # print(f"unique_dalist--{unique_dalist}")
            for  ind ,value in enumerate(unique_dalist):
                dishwbh={}
                dishwbh['title']=f"{value['TP01']}|{value['TP02']}"
                dishwbh['id'] = inde + index+ind
                dishwbh['ismw'] = '1'
                dishwbh_list.append(dishwbh)
            disrq['children'] = dishwbh_list
            # print(f"{disyf['title']}--{disrq}")
    #
            disrq_list.append(disrq)
    #
        disyf['children'] = disrq_list
        # print(disyf)
        data.append(disyf)
    # print(f'data--{data}')
    #
    #
    #
    #
    #
    #
    # print(f'data--{data}')



    # data = [
    #
    #     { 'title': '2024-07', 'id': 1,'ismw':'0', 'children': [{'title': '2024-04-13','id': 2,'children':[{'title': '01|01', 'id': 5,'ismw':'1'},{'title': '01|02', 'id': 6,'ismw':'1'}]},]},
    #     {'title': '2024-08', 'id': 3, 'ismw':'0', 'children': [{'title': '2024-04-13', 'id': 4,'ismw':'1'}]}
    # ]
   #  data = {
   # "title": "Root Node", # 根节点的名称
   #  "id": "root", # 根节点的值
   #   'ismw':2,
   #  "children": data #将原始节点作为根节点的子节点
   #  }
    return JsonResponse(data, safe=False)

def is_empty(s):
    if s is None or len(s) == 0:
        return True
    else:
        return False
def wlg_table(request):
    hwbh = request.GET.get('hwbh', '')
    gysbh = request.GET.get('cysbh', '')
    print(f'hwbh{hwbh}')
    print(is_empty(hwbh))
    if is_empty(hwbh):
        hwbh = '01'
        gysbh = '01'

    transport = Transport.objects.filter(TP01=hwbh, TP02=gysbh).values('TP01', 'TP02', 'TP03', 'TP04', 'TP05', 'TP06',
                                                                       'TP07', 'TP08', 'TP09', 'TP10', 'TP13')
    my_tran = list(transport.values())
    if is_empty(hwbh):
        hwbh = '01'
        gysbh = '01'
    logtory = Logisticstrajectory.objects.filter(LP01=hwbh, LP02=gysbh).values('LP01', 'LP02', 'LP03', 'LP04', 'LP05',
                                                                               'LP06', 'LP07', 'LP08', 'LP09', 'LP10',
                                                                               'LP11', 'LP12','LP13').order_by("LP08")
    my_logtor = list(logtory.values())
    # print(my_logtor)
    return JsonResponse({"table2_data":my_logtor,"table1_data":my_tran}, safe=False)
@csrf_exempt
def wlg_xlxg(request):
    print("修改")
    uuid = request.POST.get('uuid', '')
    # print(uuid)
    LP08 = request.POST.get('LP08', '')

    LP11=convert_date_en(LP08)
    LP12=request.POST.get('LP12', '')
    czlx = request.POST.get('CZLX', '')
    print(f'czlx{czlx}')
    if czlx=='del':
        Logisticstrajectory.objects.get(LP13=uuid).delete()
    if czlx=='edit':
        obj = Logisticstrajectory.objects.get(LP13=uuid)
        obj.LP12=LP12
        obj.LP08 = LP08
        obj.LP11 = LP11
        obj.LP20 = '2'
        obj.save()
    if czlx=='modify': # 整个路线修改
        record = Logisticstrajectory.objects.filter(LP13=uuid).values('LP01','LP02','LP08','LP10','LP12')
        record_list=list(record)
        print(f'record_list--{record_list}')
        hwbh=record_list[0]['LP01']
        gysbh = record_list[0]['LP02']
        kssj=str(record_list[0]['LP08'])
        origin =record_list[0]['LP12']
        jssj=str(LP08)
        tools = Tools()
        wlinfo=Get_wlinxfo()

        zsc=tools.datatime_sjc(kssj, jssj)
        print(f'kssja--{kssj}--{jssj}--{zsc}')
        Logisticstrajectory.objects.filter(LP08__gt=kssj,LP01=hwbh, LP02=gysbh ).delete()

        destination=LP12
        print(f'修改信息{origin}--{destination}--{hwbh}--{gysbh}--{kssj}--{zsc}')
        # wlinfo.get_ldjl(origin, destination, hwbh, gysbh, kssj, zsc)
    if  czlx=='add' :
        record = Logisticstrajectory.objects.get(LP13=uuid)
        uuidu=create_uuid()
        new_object = Logisticstrajectory.objects.create(
            LP01=record.LP01,
            LP02=record.LP02,
            LP03=record.LP03,
            LP04=record.LP04,
            LP05=record.LP05,
            LP06=record.LP06,
            LP07=record.LP07,
            LP08=LP08,
            LP09=record.LP09,
            LP10=record.LP10,
            LP11=LP11,
            LP12=LP12,
            LP13=uuidu,
            LP14=record.LP14,
            LP15=record.LP15,
            LP16=record.LP16,
            LP17=record.LP17,
            LP18=record.LP18,
            LP19=record.LP19,
            LP20='3',
        )
        new_object.save()
    data={
        "returnCode":200
    }
    return JsonResponse(data, safe=False)

@csrf_exempt
def wlg_xldel(request):
        print("删除")
        uuid = request.POST.get('uuid', '')
        Logisticstrajectory.objects.get(LP13=uuid).delete()


        data = {
            "returnCode": 200
        }
        return JsonResponse(data, safe=False)

# return HttpResponse(200)

