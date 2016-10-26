from django.contrib import admin
from mybbs import models

class BBS_admin(admin.ModelAdmin):
    list_display=('tit','summ','aut','sig','vie','cat','cre')
    list_filter=('created_at',)
    search_fields=('title','author__user__username')
    def sig(self,obj):
        return obj.author.signature
    def tit(self,obj):
        return obj.title
    def aut(self,obj):
        return obj.author
    def summ(self,obj):
        return obj.summary
    def vie(self,obj):
        return obj.view_count
    def cre(self,obj):
        return obj.created_at
    def cat(self,obj):
        return obj.category
    sig.short_description='签名'
    tit.short_description='主题'
    aut.short_description='作者'
    summ.short_description='简介'
    vie.short_description='浏览数'
    cat.short_description='版块'
    cre.short_description='创建日期'

admin.site.register(models.BBS,BBS_admin)
admin.site.register(models.Category)
admin.site.register(models.BBS_user)
