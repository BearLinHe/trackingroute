from django.contrib import admin

# Register your models here.
# 超级用户的密码 123456  admin
from index.models import Users, label, Novel, Dynamic, Comment, Purchase, Read, Xsxjpj


#
# 用户注册
class  UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'yhqx', 'qq', 'weChat','mobile')
    search_fields = ('username', 'email')  # 设置'name', 'email'字段查询显示
    list_filter = ('username',)  # 设置表'age'字段过滤
    ordering = ['mobile', ]  # 设置字段'email'排序
    list_per_page = 30  # 设置数据记录分页30条
    fieldsets = (['Main', {
        'fields': ('username', 'email', 'yhqx', 'qq', 'weChat','mobile'), }],
                 ['Advance', {
                     # 'classes': ('collapse',),
                     'fields': ('gender',), }]
                 )
admin.site.register(Users, UsersAdmin)
# 小说分类
class TagInline(admin.TabularInline):
    model = Novel
    extra = 5  # extra 参数指定了默认行的数量
class labelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  #
    search_fields = ('name',)  #
    list_filter = ('name',)  # 设置表'age'字段过滤
    inlines = [TagInline]  # 设置内联显示
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(label, labelAdmin)

# 小说信息
class  NovelAdmin(admin.ModelAdmin):
    list_display = ('bookid','name', 'singer', 'type', 'zjnum', 'zjtitle', 'xsbh')
    search_fields = ('name', 'singer', 'type', 'zjtitle')  #
    list_filter = ('name','singer','zjtitle')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['bookid', ]
admin.site.register(Novel, NovelAdmin)

# 小说动态
class DynamicAdmin(admin.ModelAdmin):
    list_display = ('lwxh', 'lwkf', 'lwzs', 'lwhc', 'tjsl', 'ypsl')
    search_fields = ('lwxh', 'lwkf', 'lwzs', 'lwhc')  #

    list_filter = ('lwxh', 'lwkf', 'lwzs','lwhc','tjsl','ypsl')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(Dynamic, DynamicAdmin)


# 小说动态
class CommentAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'bookid', 'name', 'plrq', 'content')
    search_fields = ('userid', 'username', 'bookid', 'name', 'plrq', 'content')  #

    list_filter = ('userid', 'username', 'bookid', 'name', 'plrq', 'content')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(Comment, CommentAdmin)
# 购买信息
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'xsbh', 'name', 'gmrq', 'sfgm')
    search_fields = ('userid', 'username', 'xsbh', 'name', 'gmrq', 'sfgm')  #

    list_filter = ('userid', 'username', 'xsbh', 'name', 'gmrq', 'sfgm')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(Purchase, PurchaseAdmin)

# 阅读信息
class ReadAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'xsbh', 'name', 'ydzj', 'ydid','xszj','sfwj','type')
    search_fields = ('userid', 'username', 'xsbh', 'name', 'ydzj', 'ydid','xszj','sfwj','type')  #

    list_filter = ('userid', 'username', 'xsbh', 'name', 'ydzj', 'ydid','xszj','sfwj','type')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(Read, ReadAdmin)

# 小说评星
class XsxjpjAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'xsbh', 'xjsl', 'pjrq')
    search_fields = ('userid', 'username', 'xsbh', 'xjsl', 'pjrq')  #

    list_filter = ('userid', 'username', 'xsbh', 'xjsl', 'pjrq')  # 设置表'age'字段过滤
    list_per_page = 30  # 设置数据记录分页30条
    ordering = ['id', ]
admin.site.register(Xsxjpj, XsxjpjAdmin)