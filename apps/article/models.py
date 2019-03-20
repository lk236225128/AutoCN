from django.db import models
import datetime


# Create your models here.

class Article(models.Model):
    articleName = models.CharField(max_length=50, null=False, verbose_name="文章标题")
    author = models.CharField(max_length=50, null=False, verbose_name="作者")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间 ")
    aritcleDescription = models.TextField(verbose_name="文章简述", null=True)
    aritcleContent = models.TextField(verbose_name="文章内容")
    articleImg = models.ImageField(upload_to="static/img/system/%Y/%m", verbose_name="封面图", max_length=100)

    class Meta:
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.articleName