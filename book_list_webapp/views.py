import requests
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Books
from .forms import AddBooksForm, SearchBooksForm, SearchByISBN


class BooksListView(View):
    def get(self, request):
        books = Books.objects.all()
        search_form = SearchBooksForm
        ctx = {
            "books": books,
            "search_form": search_form,
        }
        return render(request, "index.html", ctx)

    def post(self, request):
        search_form = SearchBooksForm(request.POST)
        books = Books.objects.all()
        if search_form.is_valid():
            title = search_form.cleaned_data["title"]
            author = search_form.cleaned_data["author"]
            publication_date_from = search_form.cleaned_data["publication_date_from"]
            publication_date_to = search_form.cleaned_data["publication_date_to"]
            publication_language = search_form.cleaned_data["publication_language"]
            if publication_date_from is None:
                publication_date_from = "1000-01-01"
            else:
                pass
            if publication_date_to is None:
                publication_date_to = "2999-12-31"
            else:
                pass
            if len(publication_language) == 0:
                results = (
                    Books.objects.filter(title__icontains=title)
                    .filter(author__icontains=author)
                    .filter(
                        publication_date__range=[
                            publication_date_from,
                            publication_date_to,
                        ]
                    )
                )
                ctx = {
                    "search_form": search_form,
                    "results": results,
                }
                return render(request, "index.html", ctx)
            elif len(publication_language) != 0:
                results = (
                    Books.objects.filter(title__icontains=title)
                    .filter(author__icontains=author)
                    .filter(
                        publication_date__range=[
                            publication_date_from,
                            publication_date_to,
                        ]
                    )
                    .filter(publication_language__in=publication_language)
                )
                ctx = {
                    "search_form": search_form,
                    "results": results,
                }
                return render(request, "index.html", ctx)
        else:
            messages.error(
                request, "Oops! Something went wrong. Check form input and try again."
            )
            return render(
                request,
                "index.html",
                {"books": books, "search_form": search_form},
            )


class AddBooksView(View):
    def get(self, request):
        form = AddBooksForm
        return render(request, "add_books.html", {"form": form})

    def post(self, request):
        form = AddBooksForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            publication_date = form.cleaned_data["publication_date"]
            ISBN = form.cleaned_data["ISBN"]
            pages_count = form.cleaned_data["pages_count"]
            cover_link = form.cleaned_data["cover_link"]
            publication_language = form.cleaned_data["publication_language"].upper()
            form.save()
            messages.success(request, "Success! Book added.")
            return render(
                request,
                "add_books.html",
                {"form": form},
            )
        else:
            messages.error(
                request, "Oops! Something went wrong. Check form input and try again."
            )
            return render(
                request,
                "add_books.html",
                {"form": form},
            )


class APIBooksImport(View):

    def __init__(self, **kwargs):
        super().__init__()
        self.title = None
        self.authors = None
        self.publication_date = None
        self.isbn = None
        self.page_count = None
        self.cover_link = None
        self.publication_language = None

    def get(self, request):
        form = SearchByISBN
        return render(request, "add_books_from_api.html", {"form": form})

    def post(self, request):
        form = SearchByISBN(request.POST)
        if "search" in request.POST and form.is_valid():
            self.isbn = form.cleaned_data["isbn"]
            api_response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}"
            )
            found_book = api_response.json()
            volume_info = found_book["items"][0]["volumeInfo"]
            self.title = volume_info["title"]
            self.authors = ", ".join(volume_info["authors"])
            self.publication_date = volume_info["publishedDate"]
            self.page_count = int(volume_info["pageCount"])
            self.cover_link = volume_info["imageLinks"]["thumbnail"]
            self.publication_language = volume_info["language"].upper()

            ctx = {
                "form": form,
                "found_book": found_book,
                "title": self.title,
                "authors": self.authors,
                "publication_date": self.publication_date,
                "isbn": self.isbn,
                "page_count": self.page_count,
                "cover_link": self.cover_link,
                "publication_language": self.publication_language,
            }
            return render(request, "add_books_from_api.html", ctx)
        elif "add-book" in request.POST:
            Books.objects.create(
                title=self.title,
                author=self.authors,
                publication_date=self.publication_date,
                pages_count=self.page_count,
                ISBN=self.isbn,
                cover_link=self.cover_link,
                publication_language=self.publication_language,
            )
            return redirect("books_list_view")
        else:
            messages.error(
                request, "Oops! Something went wrong. Check form input and try again."
            )
            return render(
                request,
                "add_books_from_api.html",
                {"form": form},
            )
