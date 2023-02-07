from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from news.forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from news.models import News, Category
from .utils import MyMixin

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect('login')
        # если не хотим чтобы зарегистрированный пользователь снова вводил данные:
        # user = form.save()
        # login(request, user)
        # messages.success(request, "Вы успешно зарегистрировались")
        # return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()

    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = News  # берем модель, с которой работаем
    template_name = 'news/home_news_list.html'  # создаем шаблон (как index.html)
    context_object_name = 'news'
    paginate_by = 2

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')  # применение миксинов, файл utils
        context['mixin_prop'] = self.get_prop  # передаем миксин в контекст
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')  # выводим только
        # опубликованные новости. С помощью .select_related('category') убираем дублирующиеся запросы


# def index(request):
#     news = News.objects.all()  # сортировка выполняется в модели для админки
#     # categories = Category.objects.all() - убираем повторяющийся код, т.к. оформили
#     # его к пользовательских тегах news_tags.py
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         # 'categories': categories, убираем повторяющийся код, т.к. оформили
#         # его к пользовательских тегах news_tags.py. И убираем из контекста ниже 'categories': categories
#     }
#     return render(request, template_name='news/index.html', context=context)

class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False  # запрещаем показ пустых страниц из списка
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))  # применяем миксины,
        # файл utils

        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')
        # выводим только опубликованные новости определенной категории. С помощью .select_related('category')
        # убираем дублирующиеся запросы


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     # categories = Category.objects.all() - убираем повторяющийся код, т.к. оформили
#     # его к пользовательских тегах news_tags.py. И убираем из контекста ниже 'categories': categories
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})

class ViewsNews(DetailView):
    model = News
    context_object_name = 'news_item'  # в соответствии с шаблоном news_detail.html
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    login_url = '/admin/'  # если не авторизован, отправляет на страницу авторизации админки
    # raise_exception = True # если не авторизован, доступ запрещен (ошибка 403)


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data) # ** значит автоматическую распаковку словаря
#             news = form.save()
#             return redirect(news)  # после заполнения новости - возврат на созданную новость
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'andrey_beeline@mail.ru',
                      ['avs-1981@mail.ru'], fail_silently=False) # fail_silently=False - для отладки
            if mail:
                messages.success(request, "Письмо отправлено")
                return redirect('email')
            else:
                messages.error(request, 'Ошибка отправления')
        else:
            messages.error(request, "Ошибка ввода")
    else:
        form = ContactForm()

    return render(request, 'news/email.html', {'form': form})

