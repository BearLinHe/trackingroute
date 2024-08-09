from django.core import paginator
from django.db.models import Max, Sum,Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from index.models import Transport, Logisticstrajectory
from django.contrib import messages
from novel.settings import  *
from datetime import datetime
from django.views.decorators.clickjacking import xframe_options_exempt

from django.db.models import F, FloatField
from django.db.models.expressions import RawSQL
# Create your views here.

@xframe_options_exempt
def convert_date(date_str):
    # 解析输入的日期时间字符串
    dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    # 使用strftime来格式化输出为 mm/dd pm/am 格式
    return dt_obj.strftime('%m/%d %p').lower()
def is_empty(s):
    if s is None or len(s) == 0:
        return True
    else:
        return False
def wlgj(request):
    # hwbh='hp30207'
    # cysbh='cys40025'
    hwbh = request.POST.get('search_hpbh', '')
    cysbh = request.POST.get('search_cybh', '')
    # hwbh = request.GET.get('search_hpbh', '')
    # cysbh = request.GET.get('search_cybh', '')

    if  is_empty(hwbh):
        hwbh='hp30207'
    if  is_empty(cysbh):
        cysbh='cys40025'
    print(f'hwbh{hwbh}')
    # transport=Transport.objects.all()
    custom_func_sql = 'convert_date(%s)'


    transport=Transport.objects.filter(TP01=hwbh,TP02=cysbh).values('TP01','TP02','TP03','TP04','TP05','TP06','TP07','TP08','TP09')

    my_tran = list(transport.values())
    # print('wlgj')
    # print(transport)
    now = datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')

    logtory=Logisticstrajectory.objects.filter(LP01=hwbh,LP02=cysbh,LP08__lte=formatted_time).values('LP01','LP02','LP03','LP04','LP05','LP06','LP07','LP08','LP09','LP10','LP11','LP12').order_by("LP08")

    my_logtor = list(logtory.values())
    data = {
        "MEDIA_URL": MEDIA_URL,
        "transport": my_tran,
        "logtory":my_logtor,
    }
    # print('hp30207')
    # print(transport)
    # data={}

    if  len(my_tran)==0:
        my_tran= [{'id': 1, 'TP01': '不存在', 'TP02': '不存在', 'TP03': 'XXXX', 'TP04': 'XXXX', 'TP05': 'XXXX', 'TP06': 'XXXX', 'TP07': '不存在', 'TP08': '不存在', 'TP09': '不存在'}]
    # 5
    # return render(request, 'wlgjxx.html', {
    #     'table1_data': my_tran,
    #     'table2_data': my_logtor})

    print(my_tran)
    return render(request, 'wlgjxx_ex.html', {
        'table1_data': my_tran,
        'table2_data': my_logtor})