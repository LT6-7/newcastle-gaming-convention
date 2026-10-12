from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('hosts/', views.hosts, name='hosts'),
    path('login/', views.login_view, name='login'),
]