from haystack import indexes
from .models import MyNew

class MyNewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    publishDate = indexes.DateTimeField(model_attr='publishDate')
    
    def get_model(self):
        return MyNew
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()