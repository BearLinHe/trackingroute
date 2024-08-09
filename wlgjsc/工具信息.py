# -*-coding: utf-8 -*-
# @Time    : 2024/5/19 16:34
# @Author  : 张银昌
# @File    : 工具信息.py
# @Software: PyCharm
import datetime as dt
from wlgjsc.数据库操作 import  Mysql_gssbdb
from datetime import datetime
class Tools(object):
    def __init__(self):
        pass

    def calculate_arrival_time(self, start_time, distance, speed_in_m):
        # 将速度从千米/小时转换为小时/公里
        # 计算行驶所需总时间（单位：小时）
        total_time = distance / speed_in_m
        # 在起点时间上加上总时间来获取到达时间
        arrival_time = start_time + dt.timedelta(seconds=total_time)
        return arrival_time

    def setexl(self,ws,list ,jlbz,hpbh,cysbh):
        # Mysql_db=Mysql_gssbdb()
        # Mysql_db.del_Logisticstrajectory('hp30207','cys40025')
        Mysql_db = Mysql_gssbdb()
        Mysql_db.insert_Logisticstrajectory(list,hpbh,cysbh,jlbz)

        ws.append(list)
        return ws

    def datatime_sjc(self ,time_string1,time_string2):
        time1 = datetime.strptime(time_string1, '%Y-%m-%d %H:%M:%S')
        time2 = datetime.strptime(time_string2, '%Y-%m-%d %H:%M:%S')
        delta = time2 - time1
        seconds = delta.total_seconds()
        print(f'The difference in seconds is: {seconds}')
        return seconds
    def getis_sc(self):
        is_sc='Y'
        return  is_sc

if __name__ == '__main__':
    tools=Tools()


    tools.datatime_sjc('2024-07-15 00:00:00','2024-07-17 00:00:00')