"""BookList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from book_list_webapp.views import BooksListView, AddBooksView, BookUpdateView, BookDeleteView, APIBooksImport
from book_list_API.views import BooksListViewSet, BooksFilteredView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BooksListView.as_view(), name="books_list_view"),
    path("add_books/", AddBooksView.as_view(), name="add_books"),
    path("book_update/<int:pk>", BookUpdateView.as_view(), name="book_update"),
    path("book_confirm_delete/<int:pk>", BookDeleteView.as_view(), name="book_delete"),
    path("import_from_api/", APIBooksImport.as_view(), name="import_from_api"),
    path("api/", BooksListViewSet.as_view({"get": "list"}), name="api_books_list_view"),
    re_path(
        r"^api/filter/$", BooksFilteredView.as_view(), name="api_filtered_books_view"
    ),
]
