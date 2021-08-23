from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publication_date = models.CharField(max_length=10, null=True)
    ISBN = models.CharField(max_length=13)
    page_count = models.IntegerField(null=True)
    cover_link = models.CharField(max_length=512, null=True, blank=True)
    publication_language = models.CharField(max_length=2, null=True)
