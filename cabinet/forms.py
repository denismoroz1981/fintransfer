from django import forms

class EmailPostForm(forms.Form):
    email = forms.EmailField()

from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=("username","email")

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "ЕДРПОУ"
        self.fields['username'].help_text = "8 цифровых знаков"
        self.fields['email'].null = False
        self.fields['email'].blank = False
        self.fields['email'].label = "Е-мейл"

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd["password2"]:
            raise forms.ValidationError('Пароли не идентичны!')
        return cd["password2"]