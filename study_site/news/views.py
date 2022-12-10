from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import *
from .models import News, Category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsForm, CategoriesForm, UserRegisterForm, UserAuthenticationForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout


# Замена ф-ции index для отображения списка новостей
class HomeNews(ListView):
    paginate_by = 5
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    # extra_context = {'title': 'News List'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News List'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


'''
def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'News List',
    }
    return render(request, 'news/index.html', context=context)
'''


# Замена ф-ции get_category для отображения списка новостей по категориям

class NewsCategoryList(ListView):
    paginate_by = 5
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


'''
def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})
'''


# Замена ф-ции view_news для отображения одной новости

class ViewNews(DetailView):
    model = News
    pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


'''
def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})
'''


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'


'''
def add_news(request):
    if request.method == 'POST':
        form_news = NewsForm(request.POST)
        if form_news.is_valid():
            # news = News.objects.create(**form.cleaned_data)
            news = form_news.save()
            return redirect(news)
    else:
        form_news = NewsForm()
    return render(request, 'news/add_news.html', {'form': form_news})
'''


class CreateCat(LoginRequiredMixin, CreateView):
    form_class = CategoriesForm
    template_name = 'news/add_category.html'
    success_url = reverse_lazy('home')


'''
def add_category(request):
    if request.method == 'POST':
        form_cat = CategoriesForm(request.POST)
        if form_cat.is_valid():
            form_cat.save()
            return redirect('home')
    else:
        form_cat = CategoriesForm()
    return render(request, 'news/add_category.html', {'form': form_cat})
'''


def register(request):
    if request.method == 'POST':
        login_form = UserRegisterForm(request.POST)
        if login_form.is_valid():
            user = login_form.save()
            login(request, user)
            messages.success(request, 'Register is succesfull')
            return redirect('home')
        else:
            messages.error(request, 'Error')

    else:
        login_form = UserRegisterForm()

    return render(request, 'news/register.html', {'form': login_form})


def user_login(request):
    if request.method == 'POST':
        auth_form = UserAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login(request, user)
            return redirect('home')
    else:
        auth_form = UserAuthenticationForm()
    return render(request, 'news/login.html', {'form': auth_form})


def user_logout(request):
    logout(request)
    return redirect('login')


def send_email(request):
    if request.method == 'POST':
        feedback_form = ContactForm(request.POST)
        if feedback_form.is_valid():
            mail = send_mail(feedback_form.cleaned_data['subject'], feedback_form.cleaned_data['body'],
                             'work_test813@ukr.net', ['yaroslav2002vas@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'E-mail sended')
                return redirect('home')
            else:
                messages.error(request, 'Error')
    else:
        feedback_form = ContactForm()
    return render(request, 'news/feedback.html', {'form': feedback_form})
