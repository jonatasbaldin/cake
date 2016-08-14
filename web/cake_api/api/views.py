from api.models import Author, Article
from rest_framework import viewsets
from api.serializers import AuthorSerializer, ArticleSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """ Endpoint to consume Author data
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """ Endpoint to consume Articler data
    """
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
