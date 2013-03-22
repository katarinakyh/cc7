import datetime
from haystack.indexes import *
from haystack import indexes
from models import Post


class PostIndex(indexes.SearchIndex):
    title = indexes.CharField(document=True)

    def get_model(self):
        return PostIndex

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.filter(date_created__lte=datetime.datetime.now())
