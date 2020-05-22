from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('wishmaker', views.make_wish, name='wishmaker'),
    path('process_wish', views.process_wish),
    path('grant/<int:id>', views.grant),
    path('edit/<int:id>', views.edit),
    path('edit_wish', views.edit_wish),
    path('remove/<int:id>', views.remover),
    path('like/<int:id>', views.like_me),
    path('stats', views.stats)
]
