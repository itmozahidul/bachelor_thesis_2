from django.urls import path
from . import views
urlpatterns = [


    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('collect', views.collect, name='main'),
    path('main', views.main, name='main'),
    path('add', views.add, name='add'),
    path('k_mean', views.k_mean, name='k_mean'),
    path('evaluate', views.evaluate, name='evaluate')
]

