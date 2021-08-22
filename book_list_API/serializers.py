from rest_framework import serializers
from book_list_webapp.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = [
            "id",
            "title",
            "author",
            "publication_date",
            "ISBN",
            "pages_count",
            "cover_link",
            "publication_language",
        ]
