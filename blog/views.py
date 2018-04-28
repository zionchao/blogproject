# Create your views here.

import markdown
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.forms import ArticlePostForm
from .models import Post,Category,Tag
from comments.forms import CommentForm
import logging
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from django.views.generic import ListView,DetailView

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

# def index(request):
#     post_list=Post.objects.all()
#     return render(request,'blog/index.html',context={
#         'post_list':post_list
#     })
    # return render(request,'blog/index.html',context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页'
    # })
    # return HttpResponse('Hi,欢迎访问我的博客首页！')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response=super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post=super(PostDetailView,self).get_object(queryset=None)
        post.body=markdown.markdown(post.body,extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        # 记得在顶部引入 TocExtension 和 slugify
                                        TocExtension(slugify=slugify),
                                    ])
        return post

    def get_context_data(self, **kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update(
            {
                'form':form,
                'comment_list':comment_list
            }
        )
        return context


# def detail(request,pk):
#     post=get_object_or_404(Post,pk=pk)
#
#     post.increase_views()
#
#     post.body=markdown.markdown(
#         post.body,extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc',
#         ]
#     )
#     form=CommentForm()
#     comment_list=post.comment_set.all()
#     context={
#         'post':post,
#         'form':form,
#         'comment_list':comment_list,
#     }
#     return render(request,'blog/detail.html',context=context)

# def archives(request,year,month):
#     post_list=Post.objects.filter(create_time__year=year,
#                                   create_time__month=month,
#                                   ).order_by('-create_time')
#     return render(request,'blog/index.html',context={
#         'post_list':post_list
#     })

class ArchivesView(IndexView):

    def get_queryset(self):
        # year=self.kwargs.get['year']
        # month=self.kwargs.get['month']
        # return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
        #                                                       create_time__month=month)

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month)

# def catetory(request,pk):
#     cate=get_object_or_404(Category,pk=pk)
#     post_list=Post.objects.filter(category=cate).order_by('-create_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

class  CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(pk=self.kwargs.get('pk'))

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

#csrf解决办法  https://blog.csdn.net/heatdeath/article/details/69791347
@csrf_exempt
def article_post(request):
    if request.method=='POST':
        article_post_form=ArticlePostForm(request.POST)
        print(article_post_form)
        if article_post_form.is_valid():
            cd=article_post_form.cleaned_data
            try:
                article_post_form.save()
                # new_article=article_post_form.save(commit=False)
                # print(new_article+'-----')
                # # new_article.author=request.user
                # # new_article.column=request.user.article_column.get(id=request.POST['column_id'])
                # new_article.save()
                return HttpResponse(1)#跳转到index界面
            except:
                # print('error-----')
                return HttpResponse(2)
        else:
            return HttpResponse(3)
    else:
        article_post_form=ArticlePostForm()
        article_columns=Category.objects.all()
        article_tags=Tag.objects.all()
        return render(request,'blog/publish_article.html',{'aritcle_post_form':article_post_form,
                                                           'article_coloumns':article_columns,
                                                           'article_tags':article_tags})