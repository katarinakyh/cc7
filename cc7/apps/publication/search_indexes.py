"""
import datetime
from haystack.indexes import *
from haystack import site
from models import Post


class PostIndex(SearchIndex):
    body = CharField(document=True, use_template=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.filter(date_created__lte=datetime.datetime.now())


site.register(Post, PostIndex)

"""