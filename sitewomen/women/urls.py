from django.urls import path, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('addpost/', views.AddPost.as_view(), name='add_post'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.WomenTags.as_view(), name='tag'),
    path('update/<int:pk>/', views.UpdatePost.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete_page'),

]
