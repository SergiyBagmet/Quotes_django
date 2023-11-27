from django.db import models


# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=255, unique=True, null=False)
    birth_date = models.CharField(max_length=255)
    birth_place = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
