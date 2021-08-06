from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Bloghome"),
    path('blogpost/<int:id>', views.blogpost, name="BlogPost")
]