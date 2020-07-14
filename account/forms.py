from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=8, min_length=8)
    password = forms.CharField(widget=forms.PasswordInput)