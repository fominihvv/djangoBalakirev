# -*- coding: utf-8 -*-
# sitewomen\women\views.py
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from unidecode import unidecode

from .models import Women

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
    {'id': 4, 'name': 'Журналистки'},
]


def index(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.objects.filter(is_published=True),
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'О сайте',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/about.html', context=data)


def show_post(request: HttpRequest, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)

    ### DEBUG
    slug = slugify(unidecode(post.title))
    print('women/views.py - show_post')
    print(slug, post.title)
    ###

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 0,
    }
    return render(request, 'women/show_post.html', context=data)


def addpage(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'women/addpage.html', context=data)


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


def show_category(request: HttpRequest, cat_id: int) -> HttpResponse:
    data = {
        'title': f'{cats_db[cat_id - 1]["name"]}',
        'menu': menu,
        'cat_selected': cat_id,
    }
    return render(request, 'women/show_category.html', context=data)
