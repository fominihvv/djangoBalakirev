# -*- coding: utf-8 -*-
# sitewomen\women\views.py
from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, DeleteView, UpdateView

from .forms import AddPostForm
from .models import Women, TagPost, Category

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

default_context: dict[str, Any] = {
    'menu': menu,
    'cat_selected': None,
}


class AddPost(FormView):
    template_name = 'women/add_post.html'
    form_class = AddPostForm
    # success_url = reverse_lazy('home')
    extra_context = default_context.copy()
    extra_context['title'] = 'Добавление статьи'

    def form_valid(self, form: AddPostForm) -> HttpResponse:
        form.save()
        return redirect('home')
        # return super().form_valid(form)


class WomenHome(ListView):
    # model = Women #Не использовать этот способ, если определен get_queryset
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = default_context.copy()
    extra_context['title'] = 'Главная страница'
    extra_context['cat_selected'] = 0

    def get_queryset(self) -> QuerySet:
        return Women.published.all().select_related('cat')


class AboutView(TemplateView):
    template_name = 'women/about.html'
    extra_context = default_context.copy()
    extra_context['title'] = 'О сайте'


class ContactView(TemplateView):
    template_name = "women/contact.html"
    extra_context = default_context.copy()
    extra_context['title'] = "Обратная связь"


class LoginView(TemplateView):
    template_name = 'women/login.html'
    extra_context = default_context.copy()
    extra_context['title'] = 'Авторизация'


class ShowPost(DetailView):
    # model = Women #Не использовать этот способ, если определен get_queryset
    template_name = 'women/show_post.html'
    extra_context = default_context.copy()
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self) -> QuerySet:
        return Women.published.all()

    def get_object(self, queryset: QuerySet = None) -> QuerySet:
        return get_object_or_404(queryset or self.get_queryset(), slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = default_context.copy()

    def get_queryset(self) -> QuerySet:
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        context['title'] = 'Категория: ' + category.name
        context['cat_selected'] = category.pk
        return context


class WomenTags(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = default_context.copy()

    def get_queryset(self) -> QuerySet:
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        return context


class CreatePost(CreateView):
    template_name = 'women/add_post.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')  # Если не указывать, то идёт редирект на саму статью используя get_absolute_url
    extra_context = default_context.copy()
    extra_context['title'] = 'Добавление статьи'


class DeletePost(DeleteView):
    model = Women
    template_name = 'women/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    extra_context = default_context.copy()
    extra_context['title'] = 'Удаление статьи'


class UpdatePost(UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/add_post.html'
    success_url = reverse_lazy('home')  # Если не указывать, то идёт редирект на саму статью используя get_absolute_url
    extra_context = default_context.copy()
    extra_context['title'] = 'Редактирование статьи'
