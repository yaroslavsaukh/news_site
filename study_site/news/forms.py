from django import forms
from .models import News, Category
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={"class": "form-control"}))
    body = forms.CharField(label='Body', widget=forms.Textarea(attrs={"class": "form-control"}))
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class": "form-control"}))
    captcha = CaptchaField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Password', help_text='Password must contain at least 8 characters',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-select"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Title can`t starts with number')
        return title

    '''
    title = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Description', required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
    is_published = forms.BooleanField(label='Published', initial=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', empty_label='Choose category',
                                      widget=forms.Select(attrs={"class": "form-select"}))
                                      '''


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Category name can`t starts with number')
        return title
