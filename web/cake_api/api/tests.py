import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from .models import Author, Article


class APIViewsAuthor(APITestCase):
    fixtures = ['api_author_data.json']

    def test_authors(self):
        resp = self.client.get('/api/v1/authors/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_authors_detailed(self):
        resp = self.client.get('/api/v1/authors/1/')
        data = {'id': 1,
                'name': 'Darrell Etherington',
                'profile_page': 'https://techcrunch.com/author/darrell-etherington/',
                'twitter_page': 'https://twitter.com/etherington'}
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, data)


class APIViewsArticle(APITestCase):
    fixtures = ['api_author_data.json', 'api_article_data.json']

    def test_articles(self):
        resp = self.client.get('/api/v1/articles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_articles_detailed(self):
        resp = self.client.get('/api/v1/articles/1/')
        data = {'id': 1,
                'title': "No Man's Sky is an immersive wonder for",
                'content': 'This is a brief content!',
                'url': 'https://techcrunch.com/2016/08/09/no-mans-sky-is-an-immersive-wonder-for-solitary-wanderers/',
                'published_date': '2016-08-09T12:56:43Z',
                'thumbnail_url': '',
                'author': 'http://testserver/api/v1/authors/1/'}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, data)


class IndexView(APITestCase):

    def test_index(self):
        resp = self.client.get('/')
        data = {'where_am_i': "You're at Cake! More information on https://github.com/jonatasbaldin/cake",
                'author': "Jonatas Baldin",
                'author_email': 'jonatas dot baldin at gmail dot com',
                'author_twitter': 'https://twitter.com/vuashhhh'}

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.content.decode(), json.dumps(data))


class AuthorModelTest(TestCase):

    def test_string_method(self):
        author = Author(name='Stephen King')
        self.assertEqual(str(author), author.name)


class ArticleModelTest(TestCase):

    def test_string_method(self):
        article = Article(title='Dark Tower')
        self.assertEqual(str(article), article.title)
