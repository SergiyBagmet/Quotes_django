from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('author/<int:author_id>/', views.author_info, name='author_info'),
]
