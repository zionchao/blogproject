# -*- coding:utf-8 -*-
#__author__ = 'zhangchao_a'

from django import template
from ..models import Post,Category

register=template.Library()

@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month','DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()
