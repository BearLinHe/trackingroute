import datetime

from django.shortcuts import render
# Create your views here.
from index.models import Transport, Logisticstrajectory
from  wlgjsc.美国物流距离分割算法 import Get_wlinxfo;
from wlgjsc.数据库操作 import  Mysql_gssbdb
from  novel.settings import  *
from  wlgjsc.工具信息 import Tools

def is_empty(s):
   if s is None or len(s) == 0:
      return True
   else:
      return False
def wlgjsz(request):
   tools=Tools()
   wlinfo = Get_wlinxfo()
   Mysql_db = Mysql_gssbdb()
   hwbh = request.POST.get('hwbh', '')
   gysbh = request.POST.get('gysbh', '')
   Mysql_db.del_Logisticstrajectory(hwbh,gysbh)
   tcbh=request.POST.get('tcbh','')# 拖车编号
   kcbh=request.POST.get('kcbh','') #卡车编号
   sjxm=request.POST.get('sjxm','')#司机姓名
   sjdh=request.POST.get('phone','')#司机电话
   qd=request.POST.get('qd','')#起点
   zd=request.POST.get('zd','')#终点
   qssj=request.POST.get('qssj','')#起始时间
   jssj=request.POST.get('jssj','')#起点
   if is_empty(qssj)==False and  is_empty(jssj)==False:
      zsc= tools.datatime_sjc(qssj,jssj)
   # 保存数据
   local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   if is_empty(hwbh)==False and  is_empty(gysbh)==False:
      trans=Transport.objects.filter(TP01=hwbh,TP02=gysbh).delete()
      Transport(TP01=hwbh,TP02=gysbh,TP03=gysbh,TP04=tcbh,TP05=sjxm,TP06=sjdh,TP07=qd,TP08=zd,TP09=qssj,TP10=jssj,TP13=kcbh, TP14=local_time).save()


   origin =str(qd).strip()   #'21062 Forbes Ave Hayward CA 94545'  # 例如，Los Angeles
   destination =str(zd).strip() #'1115 Wesel Blvd Hagerstown MD 21740'  # 例如，Vancouver
   if is_empty(origin)==False and   is_empty(destination)==False:
      wlinfo.get_ldjl(origin, destination,hwbh,gysbh,qssj,zsc)
   # 查询得到数据
   #
   hwbh='hp30207'
   gysbh='cys40025'
   transport = Transport.objects.filter(TP01=hwbh, TP02=gysbh).values('TP01', 'TP02', 'TP03', 'TP04', 'TP05', 'TP06',
                                                                      'TP07', 'TP08', 'TP09','TP10','TP13')
   my_tran = list(transport.values())
   logtory = Logisticstrajectory.objects.filter(LP01=hwbh, LP02=gysbh).values('LP01', 'LP02','LP03', 'LP04','LP05', 'LP06','LP07', 'LP08', 'LP09', 'LP10','LP11','LP12').order_by("LP08")
   my_logtor = list(logtory.values())
   data = {
      "MEDIA_URL": MEDIA_URL,
      "transport": my_tran,
      "logtory": my_logtor,
   }

   return render(request, 'wlgjsz.html',  {
        'table1_data': my_tran,
        'table2_data': my_logtor})