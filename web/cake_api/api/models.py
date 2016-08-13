from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=300, unique=True)
    # limit URLs by 2048 characters
    profile_page = models.CharField(max_length=2048)
    twitter_page = models.CharField(max_length=2048, null=True)

    # Returns name when called in Shell
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.CharField(max_length=2048)
    published_date = models.DateTimeField()
    thumbnail_url = models.TextField(null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # Returns title when called in Shell
    def __str__(self):
        return self.title
