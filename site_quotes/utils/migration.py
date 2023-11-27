import os

import django
from pymongo.cursor import Cursor
from pymongo import MongoClient

from .config import mongo_uri, db_name  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_quotes.settings')
django.setup()

from quotes.models import Quote, Tag, Author  # noqa


client = MongoClient(mongo_uri)
db = client.get_database(name=db_name)

authors: Cursor = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description'],
    )

quotes: Cursor = db.quotes_of.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = len(Quote.objects.filter(quote=quote['quote']))
    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
