from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib import comments
from  django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from mybbs import models
import datetime
from django.contrib.auth.models import User
import operator
import sqlite3
from PIL import Image
from random import shuffle

a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def index(req):#首页
    global a
    shuffle(a)
    bbs_list=models.BBS.objects.all()
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':1,
                                            'number':a
                                            })



def detail(req,bbs_id):#内容页
    global a
    shuffle(a)
    bbs=models.BBS.objects.get(id=bbs_id)
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('bbs_detail.html',{'bbs_obj':bbs,
                                                 'bbs_user':bbs_user,
                                                 'bbs_categories':bbs_categories,
                                                 'number':a
                                                 })



def todetail(req,bbs_id):#浏览数+1
    bbs=models.BBS.objects.get(id=bbs_id)
    x=bbs.view_count
    a=sqlite3.connect('bbs.db')
    b=a.cursor()
    b.execute("update mybbs_bbs set view_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
    a.commit()
    a.close()
    return HttpResponseRedirect('/detail/%s'%bbs_id)



def category(req,cate_id):#版块切换
    global a
    shuffle(a)
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    if int(cate_id)==1:
        bbs_list=models.BBS.objects.all()
    else:
        bbs_list=models.BBS.objects.filter(category__id=cate_id)
    bbs_categories=models.Category.objects.all()
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':int(cate_id),
                                            'number':a
                                            })


def sub_comment(req):#提交评论
    bbs_id=req.POST.get('bbs_id')
    bbs=models.BBS.objects.get(id=bbs_id)
    x=bbs.com_count
    a=sqlite3.connect('bbs.db')
    b=a.cursor()
    b.execute("update mybbs_bbs set com_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
    a.commit()
    a.close()
    bbs.com_count=19
    com=req.POST.get('comment_content').lstrip()
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    comments.models.Comment.objects.create(
                                    content_type_id=7,
                                    site_id=1,
                                    user=bbs_user.user,
                                    comment=com,
                                    object_pk=bbs_id,
                                    submit_date=datetime.datetime.now(),
                                    )
    return HttpResponseRedirect('/detail/%s#cool'%bbs_id)



def acc_login(req):#登录验证
    username = req.POST.get('username')
    password = req.POST.get('password')
    user = auth.authenticate(username=username,password=password)
    if user is not None: 
        auth.login(req,user)
        content = '''
        Welcome %s !!!
        
        <a href='/logout/' >Logout</a>
        
         ''' % user.username
        return HttpResponseRedirect('/')
    else:
        return render_to_response('login.html',{'login_err':'用户名或密码错误!'})


def logout(req):#注销
    user = req.user
    auth.logout(req)
    return render_to_response('logout.html')

def login(req):#登录
    return render_to_response('login.html')




def bbs_pub(req):#发布页
    global a
    shuffle(a)
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('bbs_pub.html',{'bbs_user':bbs_user,
                                              'bbs_categories':bbs_categories,
                                              'number':a
                                              })



def bbs_sub(req):#提交新帖
    content=req.POST.get('content')
    title=req.POST.get('title').lstrip()
    summary=req.POST.get('summary').lstrip()
    cate_id=req.POST.get('bk')
    author=models.BBS_user.objects.get(user__username=req.user)
    category=models.Category.objects.get(id=int(cate_id))
    models.BBS.objects.create(
                                title=title,
                                summary=summary,
                                content=content,
                                author=author,
                                view_count=0,
                                zan_count=0,
                                cai_count=0,
                                com_count=0,
                                ranking=2,
                                created_at=datetime.datetime.now(),
                                updated_at=datetime.datetime.now(),
                                category=category
                                )
    return HttpResponseRedirect('/')



def register(req):#注册页
    return render_to_response('register.html')


def regio(req):#提交注册
    users=models.User.objects.all()
    username = req.POST.get('username').rstrip()
    password = req.POST.get('password')
    password=make_password(password, salt=None, hasher='default')
    email = req.POST.get('email')
    for user in users:
        if username==user.username:
            return render_to_response('register.html',{'error':'该用户已注册'})
        if email==user.email:
            return render_to_response('register.html',{'error':'该邮箱已注册'})
    user=User.objects.create(
                        username=username,
                        password=password,
                        email=email
                        )
    bbs_user = models.BBS_user.objects.create(user=user)
    return HttpResponseRedirect('/login/')





def zan(req):#首页点赞
    if req.user.id!=None:
        bbs_id=req.POST.get('bbs_id')
        bbs=models.BBS.objects.get(id=bbs_id)
        x=bbs.zan_count
        y=bbs.zan_id
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%req.user.id in y:
            b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
            y=y.replace('x%sx'%req.user.id , 'x')
        else:
            b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
            y=y+'%sx'%req.user.id
        b.execute("update mybbs_bbs set zan_id='%s' where id=%d"%(y,int(bbs_id)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/#%s'%bbs.id)

def cai(req):#首页踩
    if req.user.id!=None:
        bbs_id=req.POST.get('bbs_id')
        bbs=models.BBS.objects.get(id=bbs_id)
        x=bbs.cai_count
        y=bbs.cai_id
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%req.user.id in y:
            b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
            y=y.replace('x%sx'%req.user.id , 'x')
        else:
            b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
            y=y+'%sx'%req.user.id
        b.execute("update mybbs_bbs set cai_id='%s' where id=%d"%(y,int(bbs_id)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/#%s'%bbs.id)


def zan2(req):#内容页点赞
    bbs_id=req.POST.get('bbs_id')
    if req.user.id!=None:
        bbs=models.BBS.objects.get(id=bbs_id)
        x=bbs.zan_count
        y=bbs.zan_id
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%req.user.id in y:
            b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
            y=y.replace('x%sx'%req.user.id , 'x')
        else:
            b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
            y=y+'%sx'%req.user.id
        b.execute("update mybbs_bbs set zan_id='%s' where id=%d"%(y,int(bbs_id)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/detail/%s#cool'%bbs_id)


def cai2(req):#内容页踩
    bbs_id=req.POST.get('bbs_id')
    if req.user.id!=None:
        bbs=models.BBS.objects.get(id=bbs_id)
        x=bbs.cai_count
        y=bbs.cai_id
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%req.user.id in y:
            b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
            y=y.replace('x%sx'%req.user.id , 'x')
        else:
            b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
            y=y+'%sx'%req.user.id
        b.execute("update mybbs_bbs set cai_id='%s' where id=%d"%(y,int(bbs_id)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/detail/%s#cool'%bbs_id)



def edit(req):#账户管理页
    global a
    shuffle(a)
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    bbs_categories = models.Category.objects.all()
    return render_to_response('edit.html',{'bbs_user':bbs_user,
                                           'bbs_categories':bbs_categories,
                                           'number':a
                                           })


def editall(req):#提交账户管理表
    global a
    shuffle(a)
    username = req.POST.get('username').rstrip()
    password = req.POST.get('password')
    a2=sqlite3.connect('bbs.db')
    b=a2.cursor()
    if username!="":
        b.execute("update auth_user set username='%s' where id=%d"%(username,int(req.user.id)))
    if password!="":
        password=make_password(password, salt=None, hasher='default')
        b.execute("update auth_user set password='%s' where id=%d"%(password,int(req.user.id)))
    try:
        photo = req.FILES['file0']
        photoname = photo.name.split('.')
        if photoname[-1] in ['png','PNG','jpg','JPG','jpeg','JPEG']:
            img = Image.open(photo)
            img.save('../BBS/mybbs/static/media/head/%s'%photo.name)
            b.execute("update mybbs_bbs_user set photo='head/%s' where id=%d"%(photo.name,int(req.user.bbs_user.id)))
    except:pass
    a2.commit()
    a2.close()
    bbs_list=models.BBS.objects.all()
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':1,
                                            'number':a
                                            })



def infavor(req):#首页收藏
    bbs_id=req.POST.get('bbs_id')
    bbs = models.BBS.objects.get(id=bbs_id)
    if req.user.id!=None:
        x=req.user.bbs_user.id
        y=req.user.bbs_user.favor
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%bbs_id not in y:
            y=y+'%sx'%bbs_id
            b.execute("update mybbs_bbs_user set favor='%s' where id=%d"%(y,int(x)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/#%s'%bbs.id)


def infavor2(req):#内容页收藏
    bbs_id=req.POST.get('bbs_id')
    if req.user.id!=None:
        x=req.user.bbs_user.id
        y=req.user.bbs_user.favor
        a=sqlite3.connect('bbs.db')
        b=a.cursor()
        if 'x%sx'%bbs_id not in y:
            y=y+'%sx'%bbs_id
            b.execute("update mybbs_bbs_user set favor='%s' where id=%d"%(y,int(x)))
        a.commit()
        a.close()
    return HttpResponseRedirect('/detail/%s#cool'%bbs_id)


def favorite(req):#收藏页
    global a
    shuffle(a)
    x=req.user.bbs_user.favor
    y=x.split('x')
    bbs_list=[]
    for i in y:
        if i!="":
            try:
                bbs=models.BBS.objects.get(id=int(i))
                bbs_list.append(bbs)
            except:pass
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    return render_to_response('favorite.html',{'bbs_list':bbs_list,
                                               'bbs_user':bbs_user,
                                               'bbs_categories':bbs_categories,
                                               'number':a
                                               })



    
def outfavor(req):#取消收藏
    bbs_id=req.POST.get('bbs_id')
    x=req.user.bbs_user.id
    y=req.user.bbs_user.favor.replace('x%sx'%bbs_id , 'x')
    a=sqlite3.connect('bbs.db')
    b=a.cursor()
    b.execute("update mybbs_bbs_user set favor='%s' where id=%d"%(y,int(x)))
    a.commit()
    a.close()
    return HttpResponseRedirect('/favorite')



def zan3(req):#收藏页点赞
    bbs_id=req.POST.get('bbs_id')
    bbs = models.BBS.objects.get(id=bbs_id)
    x=bbs.zan_count
    y=bbs.zan_id
    a=sqlite3.connect('bbs.db')
    b=a.cursor()
    if 'x%sx'%req.user.id in y:
        b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
        y=y.replace('x%sx'%req.user.id , 'x')
    else:
        b.execute("update mybbs_bbs set zan_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
        y=y+'%sx'%req.user.id
    b.execute("update mybbs_bbs set zan_id='%s' where id=%d"%(y,int(bbs_id)))
    a.commit()
    a.close()
    return HttpResponseRedirect('/favorite#%s'%bbs_id)


def cai3(req):#收藏页踩
    bbs_id=req.POST.get('bbs_id')
    bbs = models.BBS.objects.get(id=bbs_id)
    x=bbs.cai_count
    y=bbs.cai_id
    a=sqlite3.connect('bbs.db')
    b=a.cursor()
    if 'x%sx'%req.user.id in y:
        b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)-1,int(bbs_id)))
        y=y.replace('x%sx'%req.user.id , 'x')
    else:
        b.execute("update mybbs_bbs set cai_count=%d where id=%d"%(int(x)+1,int(bbs_id)))
        y=y+'%sx'%req.user.id
    b.execute("update mybbs_bbs set cai_id='%s' where id=%d"%(y,int(bbs_id)))
    a.commit()
    a.close()
    return HttpResponseRedirect('/favorite#%s'%bbs_id)


def search(req):#搜索结果
    global a
    shuffle(a)
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    bbs_all = models.BBS.objects.all()
    search = req.POST.get('words')
    print(search)
    bbs_list = []
    if search !='':
        for bbs in bbs_all:
            if (search in bbs.title) or (search in bbs.summary) or (search in bbs.author.user.username):
                bbs_list.append(bbs)
    return  render_to_response('search.html',{'bbs_list':bbs_list,
                                              'bbs_user':bbs_user,
                                              'bbs_categories':bbs_categories,
                                              'number':a
                                              })


def search2(req):#收藏页搜索结果
    global a
    shuffle(a)
    bbs_categories = models.Category.objects.all()
    bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    x=req.user.bbs_user.favor
    y=x.split('x')
    bbs_all=[]
    for i in y:
        if i!="":
            try:
                bbs=models.BBS.objects.get(id=int(i))
                bbs_all.append(bbs)
            except:pass
    search = req.POST.get('words')
    bbs_list = []
    if search !='':
        for bbs in bbs_all:
            if (search in bbs.title) or (search in bbs.summary) or (search in bbs.author.user.username):
                bbs_list.append(bbs)
    return  render_to_response('search.html',{'bbs_list':bbs_list,
                                              'bbs_user':bbs_user,
                                              'bbs_categories':bbs_categories,
                                              'number':a
                                              })





def hot(req,cate_id):#最热
    global a
    shuffle(a)
    if int(cate_id)!=1:
        bbs_list=models.BBS.objects.order_by('view_count').filter(category__id=int(cate_id))
    else:
        bbs_list=models.BBS.objects.order_by('view_count').all()
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':int(cate_id),
                                            'number':a
                                            })


def new(req,cate_id):#最新
    global a
    shuffle(a)
    if int(cate_id)!=1:
        bbs_list=models.BBS.objects.order_by('created_at').filter(category__id=int(cate_id))
    else:
        bbs_list=models.BBS.objects.order_by('created_at').all()
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':int(cate_id),
                                            'number':a
                                            })


def commentwow(req,cate_id):#最多评论
    global a
    shuffle(a)
    if int(cate_id)!=1:
        bbs_list=models.BBS.objects.order_by('com_count').filter(category__id=int(cate_id))
    else:
        bbs_list=models.BBS.objects.order_by('com_count').all()
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
    else: bbs_user=None
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'cate_id':int(cate_id),
                                            'number':a
                                            })

def myidea(req):#我的帖子
    global a
    shuffle(a)
    bbs_categories = models.Category.objects.all()
    if req.user!=AnonymousUser():
        bbs_user = models.BBS_user.objects.get(user_id=req.user.id)
        bbs_list=models.BBS.objects.filter(author_id=bbs_user.id)
    else:bbs_user=None
    return render_to_response('index.html',{'bbs_list':bbs_list,
                                            'bbs_user':bbs_user,
                                            'bbs_categories':bbs_categories,
                                            'number':a
                                            })
