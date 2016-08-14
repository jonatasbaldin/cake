import json
from api.models import Author, Article
from rest_framework import viewsets
from api.serializers import AuthorSerializer, ArticleSerializer
from django.http import HttpResponse


class AuthorViewSet(viewsets.ModelViewSet):
    """ Endpoint to consume Author data
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """ Endpoint to consume Articler data
    """
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer


def index(request):
    """ The index page
    """
    data = {'where_am_i': "You're at Cake! More information on https://github.com/jonatasbaldin/cake",
            'author': "Jonatas Baldin",
            'author_email': 'jonatas dot baldin at gmail dot com',
            'author_twitter': 'https://twitter.com/vuashhhh'}
    return HttpResponse(json.dumps(data), content_type='application/json', charset='utf-8')
