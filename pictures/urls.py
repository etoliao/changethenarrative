from django.urls import path
from . import views

urlpatterns = [
    path('', views.pictures_page, name='pictures_page'),
#   path('/pictures/', views.pics_css, name='pics.css'),
]