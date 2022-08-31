""" URL dispatcher """
from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.list_all, name='list_all'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('<slug:slug>/edit', views.BlogUpdateView.as_view(), name='edit'),
    path('new', views.BlogCreateView.as_view(), name='add_new'),
    path('api_data' , views.api_data, name = 'api_data')
]
