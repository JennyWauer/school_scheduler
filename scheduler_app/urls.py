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
	path('inbox/<int:id>',views.inbox),
	path('send', views.send_message),
	path('message/<int:id>', views.open_message),
	path('new_message', views.new_message),
	path('delete_inbox_message/<int:id>', views.delete_inbox_message),
	path('delete_sent_message/<int:id>', views.delete_sent_message),
]