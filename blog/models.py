from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
# Create your models here.
from django.utils.html import strip_tags

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return  self.name


class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return  self.name


class Post(models.Model):
    title=models.CharField(max_length=70,unique=True)
    body=models.TextField()
    create_time=models.DateTimeField(auto_now_add=True)
    modified_time=models.DateTimeField(auto_now_add=True)
    excerpt=models.CharField(max_length=200,blank=True)
    views=models.PositiveIntegerField(default=0)

    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return  self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

    def save(self, *args,**kwargs):
        if not self.excerpt:
            md=markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt=strip_tags(md.convert(self.body))
        super(Post,self).save(*args,**kwargs)
