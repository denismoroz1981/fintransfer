from django import forms

class EmailPostForm(forms.Form):
    email = forms.EmailField()
