import pytest
from book_list_webapp.models import Books
from book_list_webapp.forms import SearchBooksForm, AddBooksForm


@pytest.mark.django_db
def test_main_view(client, db, db_setup):
    response = client.get("/")
    assert response.status_code == 200
    all_books = Books.objects.all()
    assert all_books.count() != 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, author, publication_date_from, publication_date_to, publication_language, result",
    (
        ("test title", "", "", "", ["PL"], True),
        ("", "author2", "", "", "", True),
        ("", "", "", "", "", True),
    ),
)
def test_search_form(
    title,
    author,
    publication_date_from,
    publication_date_to,
    publication_language,
    result,
):
    form = SearchBooksForm(
        data={
            "title": title,
            "author": author,
            "publication_date_from": publication_date_from,
            "publication_date_to": publication_date_to,
            "publication_language": publication_language,
        }
    )
    assert form.is_valid() is result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, author, publication_date, ISBN, page_count, cover_link, publication_language, result",
    (
        ("", "", "", "", "", "", "", False),
        ("book", "author", "2021-01-01", "1234567890", 123, "", "PL", True),
    ),
)
def test_add_book_form(
    title,
    author,
    publication_date,
    ISBN,
    page_count,
    cover_link,
    publication_language,
    result,
):
    form = AddBooksForm(
        data={
            "title": title,
            "author": author,
            "publication_date": publication_date,
            "ISBN": ISBN,
            "page_count": page_count,
            "cover_link": cover_link,
            "publication_language": publication_language,
        }
    )
    assert form.is_valid() is result


@pytest.mark.django_db
def add_book_to_db():
    books_count = Books.objects.count()
    form = AddBooksForm(
        data={
            "title": "save test",
            "author": "save test",
            "publication_date": "2020-01-01",
            "isbn": "1212121212",
            "page_count": "1",
            "cover_link": "",
            "publication_language": "EN",
        }
    )
    form.save()
    assert form.is_valid() is True
    assert books_count + 1
