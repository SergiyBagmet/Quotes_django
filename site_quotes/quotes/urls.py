from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('author/<int:author_id>/', views.author_info, name='author_info'),
    path('new_quote/', views.new_quote, name='new_quote'),
    path('new_author/', views.new_author, name='new_author'),
    path('tag/<str:tag_name>/', views.quotes_by_tag, name='tag_quotes')
]
