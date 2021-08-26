# Book List

## Table of contents
* [Overview](#overview)
* [Features](#features)
* [Preview](#preview)  
* [Installation](#installation)
* [Setup](#setup)
* [API endpoints](#api-endpoints)
* [Automatic tests](#auto-tests)

<a name="overview"></a>
## Overview
**Book List** is a web application made with Python web frameworks Django and Django REST.
This app allows users to manage their private library.

<a name="main features"></a>
## Features

- Store book data: title, author(s), publication date, ISBN, page count, cover image and publication language,
- Search feature allows user to filter entire book collection,
- Manual book management (adding, editing and deleting),
- Google Book API integration - allows searching and importing books,
- API  

<a name="preview"></a>
## Preview
Application is operational and fully deployed at https://book-list-webapp.herokuapp.com/

## To install, set up and run app locally:
<a name="installation"></a>
### Installation

#### Prerequisites

Python v. 3.6\
requests v. 2.26.0\
pytest v. 6.2.4\
pytest-django v. 4.4.0\
psycopg2-binary v. 2.9.1\
djangorestframework v. 3.12.4\
django-environ v. 0.4.5\
django-heroku v. 0.3.1\
Django v. 3.2.6

Clone repository to your local environment.

#### Install required packages
**>>Remember to set up virtual environment!<<**

```bash
pip install -r requirements.txt
```

#### Set up environment variables

For Linux (Windows users should use 'set' command instead of 'export'):
- set the `SECRET_KEY` variable:
  ```bash 
  export SECRET_KEY='enter_your_secret_key_here'
  ```  

- set database credentials:
  ```bash
  export DATABASE_URL='enter_your_database_url_here'
  ``` 
  
- Set `DEBUG` mode:\
ON: `export DEBUG='True'`\
or\
OFF:`export DEBUG='False'`

<a name="setup"></a>
#### Setup

Make database migration

From app's directory run:
```bash
python manage.py migrate
```

Run the app:
```bash
python manage.py runserver
```
Application should be locally accessible at http://127.0.0.1:8000/ by default

<a name="api-endpoints"></a>
## API endpoints
#### Books Viewset:
  url: https://book-list-webapp.herokuapp.com/api \
  request: GET\
  no authentication needed\
  returns viewset containing list of all books 
  
  Response example:
  ```json
  [
    {
        "id": 1,
        "title": "\"Surely You're Joking, Mr. Feynman!\": Adventures of a Curious Character",
        "author": "Richard P. Feynman",
        "publication_date": "2018-02-06",
        "ISBN": "9780393355680",
        "page_count": 352,
        "cover_link": "http://books.google.com/books/content?id=_gA_DwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        "publication_language": "EN"
    },
        {
        "id": 2,
        "title": "Gardens Of The Moon",
        "author": "Steven Erikson",
        "publication_date": "2009-07-28",
        "ISBN": "9781409083108",
        "page_count": 768,
        "cover_link": "http://books.google.com/books/content?id=02F0VIwOACsC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        "publication_language": "EN"
    },
    {
        "id": 3,
        "title": "Potop",
        "author": "Henryk Sienkiewicz",
        "publication_date": "2011",
        "ISBN": "9788373272255",
        "page_count": 936,
        "cover_link": "http://books.google.com/books/content?id=ODqjPwAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        "publication_language": "PL"
    }
   ]
  ```

#### Filter results in viewset
  
  url: https://book-list-webapp.herokuapp.com/api/filter/?{value} \
  request: GET\
  no authentication needed\
  returns book data acordingly to set filter value(s); filters can be combined (with '&' separator) \
  acceptable values:
  ```
  author=
  ```
  ```
  title=
  ```
  ```
  publication_date_from=YYYY-MM-DD
  ```
  ```
  publication_date_to=YYYY-MM-DD
  ```
  ```
  publication_language=
  # publication languages should be separated by ',' character, eg. ./api/filter/?publication_language=en,pl
  ```

<a name="auto-tests"></a>
## Automatic tests

Webapp and API have basic automatic tests prepared with pytest library

Locations in app's root directory: 
- BookList/book_list_API/tests/tests.py
- BookList/book_list_webapp/tests/tests.py

To run tests go to tests directory and run:
```bash
pytest tests.py
```
