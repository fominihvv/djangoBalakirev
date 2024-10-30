# -*- coding: utf-8 -*-
# sitewomen\women\views.py

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from .forms import AddPostForm
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


"""def handle_uploaded_file(f):
    file_name, file_extension = os.path.splitext(f.name)
    with open(f'uploads/{file_name}_{uuid.uuid4()}{file_extension}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)"""


"""def about(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'О сайте',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/about.html', context=data)"""


def show_post(request: HttpRequest, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 0,
    }
    return render(request, 'women/show_post.html', context=data)


def contact(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Обратная связь',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/contact.html', context=data)


def login(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Авторизация',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/login.html', context=data)


def show_category(request: HttpRequest, cat_slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.womens.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тег: {tag.womens}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)


class AddPage(View):
    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'cat_selected': 0,
    }

    def get(self, request: HttpRequest) -> HttpResponse:
        self.data['form'] = AddPostForm()
        return render(request, 'women/addpage.html', context=self.data)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        self.data['form'] = form
        return render(request, 'women/addpage.html', context=self.data)


class WomenHome(TemplateView):
    template_name = 'women/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.published.all().select_related('cat'),
        'cat_selected': 0,
    }


class AboutView(TemplateView):
    template_name = 'women/about.html'
    extra_context = {
        'title': 'О сайте',
        'menu': menu,
        'cat_selected': 0,
    }
