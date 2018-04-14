from django.shortcuts import render

# Create your views here.

import markdown
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Category
from comments.forms import CommentForm
import logging
# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

def index(request):
    post_list=Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={
        'post_list':post_list
    })
    # return render(request,'blog/index.html',context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页'
    # })
    # return HttpResponse('Hi,欢迎访问我的博客首页！')

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.body=markdown.markdown(
        post.body,extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    form=CommentForm()
    comment_list=post.comment_set.all()
    context={
        'post':post,
        'form':form,
        'comment_list':comment_list,
    }
    return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
    post_list=Post.objects.filter(create_time__year=year,
                                  create_time__month=month,
                                  ).order_by('-create_time')
    return render(request,'blog/index.html',context={
        'post_list':post_list
    })

def catetory(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})