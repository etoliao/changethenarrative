from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsors_page, name='sponsors_page')
]