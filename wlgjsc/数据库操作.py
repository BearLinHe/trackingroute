# -*-coding: utf-8 -*-
# @Time    : 2024/6/22 22:06
# @Author  : 张银昌
# @File    : 数据库操作.py
# @Software: PyCharm
from datetime import datetime
import uuid
import dateutil.parser
import pymysql
class  Mysql_gssbdb(object):
    def __init__(self):
       self.isscbz = 'CS'
       try:
           if  self.isscbz=='CS':
               self.db = pymysql.connect(
                   host='127.0.0.1',
                   user='root',
                   port=3306,
                   password='@Helin23537175',
                   database='novel',
                   charset='utf8'

               )


           self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

       except  Exception   as err:
           print(f"Something went wrong: {err}")
       else:
           print("MySQL connection is OK.")

    def create_uuid(self):
        return uuid.uuid4().hex

    def convert_date(self,date_str):
        # 解析输入的日期时间字符串
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        # 使用strftime来格式化输出为 mm/dd pm/am 格式
        return dt_obj.strftime('%m/%d %p').lower()

    def convert_date_en(self, date_str):
        # 解析输入的日期时间字符串
        dt_obj = dateutil.parser.parse(date_str)
        english_date = dt_obj.strftime('%d %B, %Y at %H:%M')

        # 使用strftime来格式化输出为 mm/dd pm/am 格式
        return english_date
    def getdcjc(self,dzxx):
        ls_dz=''
        li_dz=dzxx.split(',')
        if len(li_dz)>=3:
            li_dz[2]=str(li_dz[2]).replace('美国','')
            ls_dz=li_dz[1]+li_dz[2]
        else:
            ls_dz=dzxx
        return ls_dz
    def del_Logisticstrajectory(self, hpbh,syhbh):
        try:
            delsbfosql = " delete   from  index_logisticstrajectory  where   LP01='"+hpbh+"'  and LP02='"+syhbh+"'  "
            self.cursor = self.db.cursor()
            self.cursor.execute(delsbfosql)
            self.db.commit()
            self.cursor.close()
            self.db.close()
        except self.db.IntegrityError  as ec:
            print(f'异常{ec.args}')
            self.db.rollback()
            self.cursor.close()
            self.db.close()

    def insert_Logisticstrajectory(self, list,hpbh, syhbh,jlbz):
        try:
           lp11=self.convert_date_en(list[5])
           print(list[7])
           lp12 = self.getdcjc(list[7])

           LP04=str(list[1]).replace("'","")
           LP10=str(list[7]).replace("'","")
           LP13=self.create_uuid()
           insql = "insert  into  index_logisticstrajectory (LP01,LP02,LP03,LP04,LP05,LP06,LP07,LP08,LP09,LP10,LP11,LP12,LP13,LP14,LP15,LP16,LP17,LP18,LP19,LP20)   values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                       (hpbh,syhbh,list[0], LP04, list[2], list[3], list[4],list[5], list[6], LP10,lp11,lp12,LP13,'','','','','','',jlbz)
           print(insql)
           self.cursor.execute(insql)
           dismeg = {}
           try:
               self.db.commit()
               self.cursor.close()
               self.db.close()
               print('保存成功')
               dismeg['msg'] = '保存成功'
               return dismeg

           except self.db.IntegrityError as  err:
               print(f'异常失败{err.args}')
               self.db.rollback()
               self.cursor.close()
               self.db.close()
               dismeg['msg'] = '保存失败'
               return dismeg
           dismeg['msg'] = '保存成功'
           return dismeg
        except self.db.IntegrityError  as ec:
            print(f'异常{ec.args}')
            self.db.rollback()
            self.cursor.close()
            self.db.close()
        pass

