import xadmin

from .models import Article

class ArticleAdmin(object):
    list_display=['articleName','author','add_time','articleImg']

xadmin.site.register(Article,ArticleAdmin)
