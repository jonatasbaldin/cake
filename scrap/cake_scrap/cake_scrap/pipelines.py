# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import os


class CakeScrapPipeline(object):

    def __init__(self):
        """ Initial database connection
        """
        self.connection = psycopg2.connect(host='db', database='postgres',
                                           user='postgres', password=os.environ['APP_DATABASE_PASSWORD'])
        self.cursor = self.connection.cursor()

    def verify_author(self, author_name):
        """ Verifies if author already exists
        """
        sql = """SELECT name FROM api_author WHERE name = %s"""
        self.cursor.execute(sql, (author_name,))
        return self.cursor.fetchone()

    def verify_article(self, article_title):
        """ Verifies if author already exists
        """
        sql = """SELECT title FROM api_article WHERE title = %s"""
        self.cursor.execute(sql, (article_title,))
        return self.cursor.fetchone()

    def process_item(self, item, spider):
        """ Process the spiders's return
        """

        try:
            # If the author is not on the database, add it
            if not self.verify_author(item.get('author_name')):
                sql = """INSERT INTO api_author (name, profile_page, twitter_page)
                         VALUES (%s, %s, %s)"""
                self.cursor.execute(sql, (item.get('author_name'),
                                          item.get('author_profile_page'),
                                          item.get('author_twitter_page')))
                self.connection.commit()

            # If the article is not on the database, add it
            if not self.verify_article(item.get('article_title')):
                self.cursor.execute("""SELECT id FROM api_author WHERE name = %s""", (item.get('author_name'),))
                author_id = self.cursor.fetchone()

                sql = """INSERT INTO api_article (title, content, url, published_date, thumbnail_url, author_id)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                self.cursor.execute(sql, (item.get('article_title'),
                                          item.get('article_content'),
                                          item.get('article_url'),
                                          item.get('article_published_date'),
                                          item.get('article_thumbnail_url'),
                                          author_id))
                self.connection.commit()

        except psycopg2.DatabaseError as e:
            print('Could not connect to the database. Error:', e)

        return item
