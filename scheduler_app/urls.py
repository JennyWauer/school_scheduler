from django.urls import path, include     
from . import views

urlpatterns = [
	path('', views.index),
	path('register',views.add_user),
	path('create_user', views.create_user),
	path('profile', views.class_profile),
	path('login', views.user_login),
	path('all_classes',views.all_classes),
	path('add_student',views.add_student),
	path('edit_assign',views.edit_assign),
	path('student_assign',views.student_assign),
	path('delete/<int:student_id>',views.delete_student),
	path('logout',views.logout),
]