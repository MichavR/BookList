import django.db.utils
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from book_list_webapp.models import Books
from book_list_API.serializers import BooksSerializer


class Obj:
    def get_object(
        self,
        author="",
        title="",
        publication_date_from="1000-01-01",
        publication_date_to="2999-12-31",
        publication_language=None,
    ):
        try:
            if publication_language is None:
                publication_language = []
            if len(publication_language) != 0:
                return (
                    Books.objects.filter(author__icontains=author)
                    .filter(title__icontains=title)
                    .filter(
                        publication_date__range=[
                            publication_date_from,
                            publication_date_to,
                        ]
                    )
                    .filter(publication_language__in=publication_language)
                )
            else:
                return (
                    Books.objects.filter(author__icontains=author)
                    .filter(title__icontains=title)
                    .filter(
                        publication_date__range=[
                            publication_date_from,
                            publication_date_to,
                        ]
                    )
                )
        except Books.DoesNotExist:
            raise Http404


class BooksListViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Books.objects.order_by("author", "title")
        serializer = BooksSerializer(queryset, many=True)
        return Response(serializer.data)


class BooksFilteredView(APIView):
    def get(
        self,
        request,
        author="",
        title="",
        publication_date_from="1000-01-01",
        publication_date_to="2999-12-31",
        publication_language="",
    ):
        author = request.GET.get("author", "")
        title = request.GET.get("title", "")
        publication_date_from = request.GET.get("publication_date_from", "1000-01-01")
        publication_date_to = request.GET.get("publication_date_to", "2999-12-31")
        if len(request.GET.get("publication_language", "")) != 0:
            publication_language = (
                request.GET.get("publication_language", "").upper().split(",")
            )
        else:
            publication_language = request.GET.get("publication_language", "")
        try:
            books = Obj.get_object(
                request,
                author,
                title,
                publication_date_from,
                publication_date_to,
                publication_language,
            )
            serializer = BooksSerializer(books, many=True, context={"request": request})
            return Response(serializer.data)
        except django.db.utils.ProgrammingError:
            raise Http404
