from django.urls import path

from .views import index, categories, categories_id


urlpatterns = [
    path('', index, name='woman_index'),
    path('cats/', categories, name='categories'),
    path('cats/<int:cat_id>/', categories_id, name='categories_id'),

]
