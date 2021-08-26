from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publication_date = models.DateField(null=True, blank=True)
    ISBN = models.CharField(max_length=13)
    page_count = models.IntegerField(null=True)
    cover_link = models.URLField(null=True)
    publication_language = models.CharField(max_length=2, null=True)
