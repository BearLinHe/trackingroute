# -*-coding: utf-8 -*-
# @Time    : 2024/5/19 18:49
# @Author  : 张银昌
# @File    : 长距离分割算法.py
# @Software: PyCharm
import datetime
import time

import requests
from googlemaps import Client
import polyline
import datetime as dt
from datetime import datetime
from  wlgjsc.工具信息 import Tools
class Get_cjlfg(object):
    def __init__(self):
        self.tools=Tools()
        self.api_key="AIzaSyBt9hH7SC3rJu2eAchw_A-zt4Qrg2ic0Gs"
        self.gmaps = Client(key=self.api_key)
        self.start_time=""
        pass
    def get_cjldada(self,dis,ws,jlbz,hpbh,cysbh):
        self.start_time=dis['开始时间']
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={dis['origin']}&destination={dis['destination']}&key={self.api_key}&units=imperial  "
        proxy = {'http': '127.0.0.1:7897', 'https': '127.0.0.1:7897'}
        print(f"起点{dis['origin']} -- 终点 {dis['destination']}")
        if self.tools.getis_sc()=='N':
           response = requests.get(url, proxies=proxy).json()
        else:
            response = requests.get(url).json()
        if 'routes' in response and response['routes']:
            route = response['routes'][0]
            overview_polyline = route['overview_polyline']['points']

            # 解析并打印编码多边形上的所有点
            decoded_points = polyline.decode(overview_polyline)
            print(f'decoded_points--{len(decoded_points)}')
            lien=len(decoded_points)
            m=6
            if lien<=100:
                m=4
            elif lien>100 and  lien<=200:
                m=8
            elif lien > 200 and lien <= 300:
                m = 12
            elif lien > 300 and lien <= 400:
                m=16
            elif lien > 400 and lien <= 500:
                m=20
            else:
                m = 25
            parts = self.split_into_four_equal_parts(decoded_points,m)
            # print(f'parts{parts}')
            # input('')
            # parts=self.split_into_four_equal_parts_ex(decoded_points)
            origin=0
            for index ,li in enumerate(parts):
                if len(li)==0:
                   continue
                if index==0:
                   origin= f'{li[0][0]},{li[0][-1]}'
                   qsdz = self.getdz(origin)  # 起始地址

                print(f'indexorigin--{origin}')
                destination = f'{li[-1][0]},{li[-1][-1]}'
                print(f'indexdestination--{destination}')
                zddz = self.getdz(destination)  # 终点地址
                distance_matrix = self.gmaps.distance_matrix(origin, destination)
                xsjl = distance_matrix['rows'][0]['elements'][0]['distance']['text']
                dwjl = distance_matrix['rows'][0]['elements'][0]['distance']['value']
                xsys = int(dwjl / dis['每秒钟速度(米/秒)'])  # 行驶用时
                print(f'时间{self.start_time}=={xsys}')
                format = "%Y-%m-%d %H:%M:%S"
                # datetime_obj = datetime.strptime(date_str, format)
                str_time = datetime.strptime(self.start_time, format) + dt.timedelta(seconds=xsys)
                self.start_time = str_time.strftime('%Y-%m-%d %H:%M:%S')
                ret = f"起点经纬度:{origin} --起点地址{qsdz} 行驶{dwjl}米--行驶速度{dis['每秒钟速度(米/秒)']}--用时{xsys}秒--抵达时间{self.start_time}--抵达地址经纬度 {destination} --抵达地址{zddz}"
                lis_data = [origin, qsdz, dwjl, dis['每秒钟速度(米/秒)'], xsys, self.start_time, destination,
                            zddz]
                if dwjl>10000:
                    ws = self.tools.setexl(ws, lis_data,jlbz,hpbh,cysbh)
                else:
                    continue
                print(ret)
            # print(type(decoded_points))

            # for index,point in enumerate(decoded_points):
            # print(len(decoded_points))
            # print(f'{decoded_points[0]}--{decoded_points[-1]}')
            # print(f'{decoded_points[0][0]}---{decoded_points[0][-1]}')

            '''
            这是获取一条路线的
            origin=f'{decoded_points[0][0]},{decoded_points[0][-1]}'
            qsdz = self.getdz(origin)  # 起始地址
            destination = f'{decoded_points[-1][0]},{decoded_points[-1][-1]}'
            zddz = self.getdz(destination)  # 终点地址
            print(f'{origin}--{destination}')
            distance_matrix = self.gmaps.distance_matrix(origin, destination)
            print(distance_matrix)

            xsjl = distance_matrix['rows'][0]['elements'][0]['distance']['text']
            dwjl = distance_matrix['rows'][0]['elements'][0]['distance']['value']
            xsys = int(dwjl / dis['每秒钟速度(米/秒)'])  # 行驶用时
            xsys = int(dwjl / dis['每秒钟速度(米/秒)'])  # 行驶用时
            print(f'时间{self.start_time}=={xsys}')
            format = "%Y-%m-%d %H:%M:%S"
            # datetime_obj = datetime.strptime(date_str, format)
            str_time = datetime.strptime(self.start_time , format)+ dt.timedelta(seconds=xsys)
            self.start_time=str_time.strftime('%Y-%m-%d %H:%M:%S')
            ret = f"起点经纬度:{origin} --起点地址{qsdz} 行驶{dwjl}米--行驶速度{dis['每秒钟速度(米/秒)']}--用时{xsys}秒--抵达时间{self.start_time}--抵达地址经纬度 {destination} --抵达地址{zddz}"
            lis_data = [origin, qsdz, dwjl, dis['每秒钟速度(米/秒)'], xsys,self.start_time, destination,
                        zddz]
            ws = self.tools.setexl(ws, lis_data)
            print(ret)

            '''


            # origin= f"{decoded_points[0]}}"
            # input('')
            # for current_item, previous_item in zip(decoded_points, [None] + decoded_points):
            #     if previous_item is not None:
            #         # print(f"当前项: {current_item}, 前一项: {previous_item}")
            #         info = ""
            #         origin = f"{previous_item[0]},{previous_item[1]}"  # 起始坐标
            #         qsdz = self.getdz(origin)  # 起始地址
            #         time.sleep(0.5)
            #         destination = f"{current_item[0]},{current_item[1]}"  # 终点坐标
            #         time.sleep(0.5)
            #         zddz =  self.getdz(destination)  # 终点地址
            #         distance_matrix =  self.gmaps.distance_matrix(origin, destination)
            #         xsjl = distance_matrix['rows'][0]['elements'][0]['distance']['text']
            #         dwjl = distance_matrix['rows'][0]['elements'][0]['distance']['value']
            #         # info = f"起点经纬度{origin} -起始地址{qsdz} --结束坐标{destination}-- 结束地址{dz} -- 行驶距离{dwjl}"
            #         xsys= int(dwjl/dis['每秒钟速度(米/秒)']) #行驶用时
            #         print(f'时间{self.start_time}=={xsys}')
            #         format = "%Y-%m-%d %H:%M:%S"
            #         # datetime_obj = datetime.strptime(date_str, format)
            #         str_time = datetime.strptime(self.start_time , format)+ dt.timedelta(seconds=xsys)
            #         self.start_time=str_time.strftime('%Y-%m-%d %H:%M:%S')
            #         ret = f"起点经纬度:{origin} --起点地址{qsdz} 行驶{dwjl}米--行驶速度{dis['每秒钟速度(米/秒)']}--用时{xsys}秒--抵达时间{self.start_time}--抵达地址经纬度 {destination} --抵达地址{zddz}"
            #         lis_data = [origin, qsdz, dwjl, dis['每秒钟速度(米/秒)'], xsys,self.start_time, destination,
            #                     zddz]
            #         ws = self.tools.setexl(ws, lis_data)
            #         print(ret)
            decret={
                "ws":ws,
                "start_time":self.start_time
            }
            return  decret

    def split_into_four_equal_parts(self,lst,n):
        # 以前是6
        k, m = divmod(len(lst), n)
        return [lst[i * k + s: (i + 1) * k + s] for i in range(n) for s in [0, m]] if m else [lst[i * k: (i + 1) * k]
                                                                                              for i
                                                                                              in range(n)]

    def split_list(self,lst, m):
        n = len(lst)
        return [lst[i:i + n // m] for i in range(0, n, n // m)]

    def split_into_four_equal_parts_ex(self,lst):
        result = self.split_list(lst, 6)
        ret = []
        for index, sub_list in enumerate(result):
            print(f'index{index}--{sub_list}')
            if index == 0:
                print(f'{index}--{sub_list[0]}--{sub_list[-1]}')
                ret.append(sub_list[0])
                ret.append(sub_list[-1])
            else:
                ret.append(sub_list[-1])
                print(f'{index}--{sub_list[-1]}')

        return  ret


    def getdz(self,LATLNG):
            API_KEY = 'AIzaSyBt9hH7SC3rJu2eAchw_A-zt4Qrg2ic0Gs'

            # 要查询的经纬度
            # LATLNG = '33.03579421197284, 108.97317382491312'  # 例如纽约市的经纬度

            # 构建请求URL
            url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={LATLNG}&key={API_KEY}&language=zh-CN'

            # 发送HTTP请求
            # print(url)
            proxy = {'http': '127.0.0.1:7897', 'https': '127.0.0.1:7897'}
            try:
                if  self.tools.getis_sc()=="N":
                    response = requests.get(url, proxies=proxy)
                else:
                    response = requests.get(url)

                # 解析JSON响应
                data = response.json()
            except Exception:
                if self.tools.getis_sc()=="N":
                   response = requests.get(url, proxies=proxy)
                else:
                    response = requests.get(url)
                data = response.json()
            except requests.ConnectionError:
                if self.tools.getis_sc() == "N":
                    response = requests.get(url, proxies=proxy)
                else:
                    response = requests.get(url)
                data = response.json()
            except requests.RequestException:
                if self.tools.getis_sc() == "N":
                   response = requests.get(url, proxies=proxy)
                else:
                    response = requests.get(url)
                data = response.json()
            # 检查状态
            if data['status'] == 'OK':
                # 打印地址
                formatted_address = data['results'][0]['formatted_address']
                return formatted_address
                # print(formatted_address)
            else:
                print('无法获取地址')