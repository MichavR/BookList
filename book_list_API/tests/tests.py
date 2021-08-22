import pytest
from book_list_webapp.models import Books


@pytest.mark.django_db
def test_get_books_list(client, db, db_setup):
    response = client.get("/api/")
    assert response.status_code == 200
    all_books = Books.objects.all()
    assert all_books.count() != 0


@pytest.mark.django_db
def test_books_filtering(client):
    response = client.get("/api/filter/?title=title2")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "test title2"
    response = client.get("/api/filter/?author=author2")
    assert response.status_code == 200
    assert response.json()[0]["author"] == "test author2"
    response = client.get(
        "/api/filter/?publication_date_from=2020-01-01&publication_date_to=2020-02-01"
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    response = client.get("/api/filter/?publication_language=pl,en")
    assert response.status_code == 200
    assert (
        e
        for e in response.json()
        if e["publication_language"] == "EN" or e["publication_language"] == "PL"
    )
