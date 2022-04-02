from django import forms


class SearchInput(forms.Form):
    search_string = forms.CharField(label='search_string' ,max_length=200)