import requests
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView

from .models import Books
from .forms import AddBooksForm, SearchBooksForm, SearchByISBN


class BooksListView(View):
    def get(self, request):
        books = Books.objects.all().order_by("title")
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
                publication_date_from = datetime.datetime.strptime("1000-01-01", "%Y-%m-%d").date()
            if publication_date_to is None:
                publication_date_to = datetime.datetime.strptime("2999-12-31", "%Y-%m-%d").date()

            if len(publication_language) == 0:
                results = (
                    Books.objects.filter(title__icontains=title, author__icontains=author, publication_date__range=[
                            publication_date_from,
                            publication_date_to
                        ])
                )
                ctx = {
                    "search_form": search_form,
                    "results": results,
                }
                return render(request, "index.html", ctx)
            elif len(publication_language) != 0:
                results = (
                    Books.objects.filter(title__icontains=title, author__icontains=author, publication_date__range=[
                            publication_date_from,
                            publication_date_to,
                        ], publication_language__in=publication_language)
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
            isbn = form.cleaned_data["ISBN"]
            page_count = form.cleaned_data["page_count"]
            cover_link = form.cleaned_data["cover_link"]
            publication_language = form.cleaned_data["publication_language"].upper()
            form.save()
            messages.success(request, "Success! Book added.")
            return redirect("add_books")
        else:
            messages.error(
                request, "Oops! Something went wrong. Check form input and try again."
            )
            return render(
                request,
                "add_books.html",
                {"form": form},
            )


class BookUpdateView(UpdateView):
    form_class = AddBooksForm
    queryset = Books.objects.all()
    template_name = "books_update.html"
    template_name_suffix = "_update"
    success_url = "/"


class BookDeleteView(DeleteView):
    model = Books
    template_name = "books_confirm_delete.html"
    success_url = reverse_lazy("books_list_view")


class APIBooksImport(View):
    def get(self, request):
        form = SearchByISBN
        return render(request, "add_books_from_api.html", {"form": form})

    def post(self, request):
        form = SearchByISBN(request.POST)
        isbn = None
        api_response = None

        if form.is_valid():
            isbn = form.cleaned_data["isbn"]
            api_response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            )
        else:
            return messages.error(request, form.errors)
        try:
            found_book = api_response.json()
            volume_info = found_book["items"][0]["volumeInfo"]
            title = volume_info["title"]
            authors = ", ".join(volume_info["authors"])
            publication_date = volume_info["publishedDate"]
            page_count = int(volume_info["pageCount"])
            cover_link = volume_info["imageLinks"]["thumbnail"]
            publication_language = volume_info["language"].upper()
        except KeyError:
            form = SearchByISBN
            messages.error(request, "Error. Try other ISBN or add book manually.")
            return render(request, "add_books_from_api.html", {"form": form})

        if "search" in request.POST and form.is_valid():
            ctx = {
                "form": form,
                "found_book": found_book,
                "title": title,
                "authors": authors,
                "publication_date": publication_date,
                "isbn": isbn,
                "page_count": page_count,
                "cover_link": cover_link,
                "publication_language": publication_language,
            }
            return render(request, "add_books_from_api.html", ctx)
        elif "add-book" in request.POST:
            if len(publication_date) < 10:
                publication_date = None

            Books.objects.create(
                title=title,
                author=authors,
                publication_date=publication_date,
                page_count=page_count,
                ISBN=isbn,
                cover_link=cover_link,
                publication_language=publication_language,
            )
            messages.success(request, "Success! Book added.")
            return redirect("import_from_api")
        else:
            messages.error(
                request, "Oops! Something went wrong. Check form input and try again."
            )
            return render(
                request,
                "add_books_from_api.html",
                {"form": form},
            )
