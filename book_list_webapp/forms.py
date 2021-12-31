from django import forms
from .models import Books


def language_choices():
    languages_set = Books.objects.only("publication_language").distinct(
        "publication_language"
    )
    choices = []
    for language in languages_set:
        choices.append([language.publication_language, language.publication_language])
    return choices


class AddBooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = [
            "title",
            "author",
            "publication_date",
            "ISBN",
            "page_count",
            "cover_link",
            "publication_language",
        ]


class SearchBooksForm(forms.Form):
    """
    class constructor overwritten for 'publication_language' field to avoid migration issues
    caused by performing db query at class level
    """

    def __init__(self, *args, **kwargs):
        super(SearchBooksForm, self).__init__(*args, **kwargs)
        self.fields["publication_language"] = forms.MultipleChoiceField(
            choices=language_choices(), required=False
        )

    title = forms.CharField(label="Title", required=False)
    author = forms.CharField(label="Author", required=False)
    publication_date_from = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        label="Publication date from",
        required=False
    )
    publication_date_to = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        label="to",
        required=False)


class SearchByISBN(forms.Form):
    isbn = forms.CharField(label="ISBN", required=False, min_length=10, max_length=13)
