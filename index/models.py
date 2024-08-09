from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# admin 123456python
# python manage.py makemigrations index  # 创建迁移文件
# python manage.py migrate                # 应用迁移到数据库
class Users(models.Model):
    # username=models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='用户名称')
    username = models.CharField(blank=True, max_length=128, verbose_name='姓名')
    password = models.CharField(blank=True,max_length=128, verbose_name='密码')
    email = models.CharField(blank=True,max_length=254, verbose_name='邮箱地址')
    yhqx = models.CharField(blank=True,max_length=20, verbose_name='用户权限')
    qq = models.CharField(blank=True,max_length=20, verbose_name='用户的QQ号码')
    weChat = models.CharField(blank=True,max_length=20, verbose_name='用户的微信号码')
    mobile = models.CharField(blank=True,max_length=25, verbose_name='用户的手机号码')
    choices = (
        ('male', '男性'),
        ('female', '女性'),
    )
    gender = models.CharField(max_length=8, choices=choices, default='male', verbose_name='性别')

    class Meta:  # 在admin 界面显示中文名称
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
class label(models.Model):
    name = models.CharField(verbose_name='分类标签', max_length=50)

    def __str__(self):  # 使用查询显示名称
        return f'<{self.name}>'

    class Meta:  # 在admin 界面显示中文名称
        verbose_name = '小说分类'
        verbose_name_plural = '小说分类'

'''
| 表字段 | 字段类型              | 含义           |
| ------ | --------------------- | -------------- |
| id     | Int类型，长度为11     | 主键           |
| name   | Varchar类型，长度为10 | 小说分类标签 |
'''





'''
小说信息
| 表字段    | 字段类型               | 含义                 |
| --------- | ---------------------- | -------------------- |
| id        | Int类型，长度为11      | 主键                 |
| name      | Varchar类型，长度为50  | 小说名称             |
| singer    | Varchar类型，长度为50  | 小说作家       |
| type      | Varchar类型，长度为50  | 小说的风格类型       |
| zjnum      | Varchar类型，长度为50  | 小说的章节数量      |
| zjzs      | Varchar类型，长度为50  | 小说的章节字数      |
| zjmul      | Varchar类型，长度为50  | 小说目录      |
| zjtitle     | Varchar类型，长度为50  | 小说的章节题目      |
| zjbh     | Varchar类型，长度为50  | 小说的章节编号 10-001-001      |
| img       | Varchar类型，长度为100 | 小说的封面图片路径     |
| fil       | Varchar类型，长度为100 | 小说文章路径     |
| label_id  | Int类型，长度为11      | 外键，关联歌曲分类表
'''
class Novel(models.Model):
    bookid = models.CharField(verbose_name='小说编号', max_length=200)
    name = models.CharField(verbose_name='小说名',max_length=200)
    singer = models.CharField(verbose_name='作者', max_length=200)
    type = models.CharField(verbose_name='分类', max_length=200)
    zjnum = models.CharField(verbose_name='章节数量', max_length=200)
    zjtitle = models.CharField(verbose_name='章节标题', max_length=200)
    xsbh = models.CharField(verbose_name='章节编号', max_length=200)
    img = models.FileField(verbose_name='封面', upload_to='noveimage/')
    file = models.FileField(verbose_name='文章路径', upload_to='novefile/')
    iswj = models.CharField(verbose_name='是否完结', max_length=20, default='是')
    fbrq = models.CharField(verbose_name='发布日期', max_length=20, default='')
    label_id = models.ForeignKey(label, verbose_name='分类',on_delete=models.CASCADE)
    def __str__(self): #使用查询显示名称
          return  f'<{self.name}>'
    class Meta:#在admin 界面显示中文名称
          ordering = ['bookid']
          verbose_name='小说信息'
          verbose_name_plural='小说信息'
# 歌曲动态表
class Dynamic(models.Model):
    # novel_id = models.OneToOneField(Novel,verbose_name='小说名',on_delete=models.CASCADE)
    lwxh =  models.IntegerField(verbose_name='阅读数量',default=0)
    lwkf = models.IntegerField(verbose_name='下载数量', default=0)
    lwzs = models.IntegerField(verbose_name='购买数量', default=0)
    lwhc = models.IntegerField(verbose_name='礼物数量', default=0)
    tjsl = models.IntegerField(verbose_name='推荐数量', default=0)
    ypsl = models.IntegerField(verbose_name='月票数量', default=0)
    xjsl = models.IntegerField(verbose_name='星级数量', default=0)
    bookid = models.CharField (verbose_name='小说编号', max_length=20,default='')
    class Meta:#在admin 界面显示中文名称
          verbose_name='小说动态'
          verbose_name_plural='小说动态'
    '''
    | 表字段   | 字段类型          | 1
    含义                 |
| -------- | ----------------- | -------------------- |
| id       | Int类型，长度为11 | 主键                 |
| lwxh    | Int类型，长度为11 | 礼物鲜花数量       |
| lwkf   | Int类型，长度为11 | 礼物咖啡数量       |
| lwzs | Int类型，长度为11 | 礼物咖啡数量       |
| lwhc | Int类型，长度为11 | 礼物豪车数量       |
| tjsl | Int类型，长度为11 | 推荐数量       |
| ypsl | Int类型，长度为11 | 月票数量       |
| novel_id  | Int类型，长度为11 | 外键，关联歌曲信息表 |
    '''

# 歌曲动态表
class Purchase(models.Model):
    userid = models.CharField(verbose_name='用户ID', max_length=50)
    username = models.CharField(verbose_name='用户姓名', max_length=50)
    xsbh = models.CharField(verbose_name='小说编号', max_length=50)
    name = models.CharField(verbose_name='小说名称', max_length=50)
    gmrq = models.CharField(verbose_name='购买日期', max_length=50,default='')
    sfgm = models.CharField(verbose_name='是否购买', max_length=50)
    class Meta:#在admin 界面显示中文名称
          verbose_name='购买信息'
          verbose_name_plural='购买信息'
    '''
    | 表字段   | 字段类型          | 含义                 |
| -------- | ----------------- | -------------------- |
| id       | Int类型，长度为11 | 主键                 |
| userid    | Int类型，长度为11 | 用户ID       |
| username   | Int类型，长度为11 | 用户姓名       |
| xsbh | Varchar类型，长度为100 | 小说编号       |
| name | Varchar类型，长度为100 | 小说名称       |
| sfgm | Varchar类型，长度为100 | 是否购买       |

    '''

class Comment(models.Model):
    userid = models.CharField(verbose_name='用户ID', max_length=50)
    username = models.CharField(verbose_name='用户姓名', max_length=50)
    bookid = models.CharField(verbose_name='小说编号', max_length=50)
    name = models.CharField(verbose_name='小说名称', max_length=50)
    plrq = models.CharField(verbose_name='评论日期', max_length=50)
    content = models.CharField(verbose_name='评论内容', max_length=500)
    class Meta:#在admin 界面显示中文名称
          verbose_name='评论信息'
          verbose_name_plural='评论信息'

class Read(models.Model):
    userid = models.CharField(verbose_name='用户ID', max_length=50)
    username = models.CharField(verbose_name='用户姓名', max_length=50)
    xsbh = models.CharField(verbose_name='小说编号', max_length=50)
    name = models.CharField(verbose_name='小说名称', max_length=50)
    ydzj = models.CharField(verbose_name='阅读章节', max_length=50)
    ydid = models.CharField(verbose_name='阅读的小说id', max_length=50)
    xszj = models.CharField(verbose_name='小说章节', max_length=50)
    sfwj = models.CharField(verbose_name='是否完结', max_length=50)
    type = models.CharField(verbose_name='小说类型', max_length=50)
    class Meta:#在admin 界面显示中文名称
          verbose_name='阅读信息'
          verbose_name_plural='阅读信息'

class Xsxjpj(models.Model):
    userid = models.CharField(verbose_name='用户ID', max_length=50)
    username = models.CharField(verbose_name='用户姓名', max_length=50)
    xsbh = models.CharField(verbose_name='小说编号', max_length=50)
    xjsl = models.IntegerField(verbose_name='星级数量', default=0)
    pjrq = models.CharField(verbose_name='评价日期', max_length=50)

    class Meta:  # 在admin 界面显示中文名称
        verbose_name = '小说评星'
        verbose_name_plural = '小说评星'
# 物流轨迹运输信息

class Transport(models.Model):
    TP01 = models.CharField(verbose_name='货物编号', max_length=50)
    TP02 = models.CharField(verbose_name='承运商编号', max_length=50)
    TP03 = models.CharField(verbose_name='承运人名称', max_length=50)
    TP04 = models.CharField(verbose_name='拖车', max_length=50)
    TP05 = models.CharField(verbose_name='司机', max_length=50)
    TP06 = models.CharField(verbose_name='司机电话', max_length=50)
    TP07 = models.CharField(verbose_name='始发站', max_length=400)
    TP08 = models.CharField(verbose_name='目的站', max_length=400)
    TP09 = models.CharField(verbose_name='发货日期', max_length=25)
    TP10 = models.CharField(verbose_name='操作日期', max_length=25)
    TP11 = models.CharField(verbose_name='操作人', max_length=50)
    TP12 = models.CharField(verbose_name='备注', max_length=200)
    TP13 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP14 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP15 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP16 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP17 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP18 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP19 = models.CharField(verbose_name='备用字段一', max_length=200)
    TP20 = models.CharField(verbose_name='备用字段一', max_length=200)
    class Meta:  # 在admin 界面显示中文名称
        verbose_name = '物流轨迹信息'
        verbose_name_plural = '物流轨迹'
# 物流轨迹信息
class Logisticstrajectory(models.Model):
      LP01 = models.CharField(verbose_name='货物编号', max_length=50)
      LP02 = models.CharField(verbose_name='承运商编号', max_length=50)
      LP03 = models.CharField(verbose_name='起点经度', max_length=50,default='',blank=True)
      LP04 = models.CharField(verbose_name='起点地址', max_length=400,default='',blank=True)
      LP05 = models.CharField(verbose_name='行驶速度', max_length=50,default='',blank=True)
      LP06 = models.CharField(verbose_name='行驶距离', max_length=50,default='',blank=True)
      LP07 = models.CharField(verbose_name='行驶用时', max_length=50,default='',blank=True)
      LP08 = models.CharField(verbose_name='抵达时间', max_length=50,default='',blank=True)
      LP09 = models.CharField(verbose_name='终点经纬度', max_length=50,default='',blank=True)
      LP10 = models.CharField(verbose_name='终点地址', max_length=400,default='',blank=True)
      LP11 = models.CharField(verbose_name='备用字段', max_length=50 ,default='',blank=True)
      LP12 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP13 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP14 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP15 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP16 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP17 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP18 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP19 = models.CharField(verbose_name='备用字段', max_length=50,default='',blank=True)
      LP20 = models.CharField(verbose_name='备用字段一', max_length=50,default='',blank=True)

      class Meta:  # 在admin 界面显示中文名称
          verbose_name = '谷歌物流轨迹信息'
          verbose_name_plural = '谷歌物流轨迹'
          index_together = [
              ['LP01', 'LP02','LP07','LP09'],
          ]

# 权限
class wlglqx(models.Model):
    LP01 = models.CharField(verbose_name='功能代码', max_length=50)
    LP02 = models.CharField(verbose_name='功能名称', max_length=50)
    LP03 = models.CharField(verbose_name='功能级次', max_length=50, default='', blank=True)
    LP04 = models.CharField(verbose_name='启用标志', max_length=400, default='', blank=True)
    LP05 = models.CharField(verbose_name='顺序', max_length=50, default='', blank=True)
    LP06 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP07 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP08 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP09 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP10 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP11 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP12 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP13 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP14 = models.CharField(verbose_name='备用字段', max_length=50, default='', blank=True)
    LP15 = models.CharField(verbose_name='备用字段一', max_length=50, default='', blank=True)

    class Meta:  # 在admin 界面显示中文名称
        verbose_name = '物流管理主界面'
        verbose_name_plural = '物流管理主界面'
        index_together = [
            ['LP01', 'LP02'],
        ]