from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/<int:pk>/', views.quote_detail, name='quote_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('add/author/', views.add_author, name='add_author'),
    path('add/quote/', views.add_quote, name='add_quote'),
    path('add/tag/', views.add_tag, name='add_tag'),
] 