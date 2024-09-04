from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
           {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
           {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
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
        'posts': data_db,
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


def show_post(request: HttpRequest, post_id: int) -> HttpResponse:
    content = None
    for post in data_db:
        if post['id'] == post_id:
            content = post
            break
    if content is None:
        raise Http404()
    data = {
        'title': content['title'],
        'menu': menu,
        'data': content['content'],
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
