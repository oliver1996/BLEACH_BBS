from django.db import models
from django.contrib.auth.models import User

class BBS(models.Model):
    title   =   models.CharField(max_length=64)
    summary =   models.CharField(max_length=256,blank=True,null=True)
    content =   models.TextField()
    author  =   models.ForeignKey('BBS_user')
    category = models.ForeignKey('Category')
    view_count  =  models.IntegerField()
    ranking =   models.IntegerField()
    created_at  =  models.DateTimeField(auto_now_add=True)
    updated_at  =  models.DateTimeField(auto_now_add=True)
    zan_count = models.IntegerField()
    cai_count = models.IntegerField()
    com_count = models.IntegerField()
    zan_id = models.TextField(default='x')
    cai_id = models.TextField(default='x')
    def __str__(self):
        return self.title


class Category(models.Model):
    name   =   models.CharField(max_length=32,unique=True)
    administrator = models.ForeignKey('BBS_user')
    def __str__(self):
        return self.name


class BBS_user(models.Model):
    user = models.OneToOneField(User)
    signature = models.CharField(max_length=128,default='This guy is too lazy to leave anything here.')
    photo = models.ImageField(upload_to='head',default='head/photo.jpg')
    favor = models.TextField(default='x')
    def __str__(self):
        return self.user.username


