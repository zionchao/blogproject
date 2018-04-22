# -*- coding:utf-8 -*-
#__author__ = 'zhangchao_a'

from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count

register=template.Library()

@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all()[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month','DESC')

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # return Category.objects.all()

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
