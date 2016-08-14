from api.models import Author, Article
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializers Author data
    """
    class Meta:
        model = Author
        fields = ('id', 'name', 'profile_page', 'twitter_page')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializers Article data
    """
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'url', 'published_date',
                  'thumbnail_url', 'author')
