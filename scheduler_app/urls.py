from django.urls import path, include     
from . import views

urlpatterns = [
	path('', views.index),
	path('register',views.add_user),
	path('create_user', views.create_user),
	path('profile', views.class_profile),
	path('login', views.user_login),
	path('logout',views.logout),
]