from django.urls import path, include     
from . import views

urlpatterns = [
	path('', views.index),
	path('register',views.add_user),
	path('create_user', views.create_user),
	path('profile', views.profile),
	path('create_subject', views.create_subject),
	path('subjects/<int:subject_id>', views.subject_page),
	path('subjects/<int:subject_id>/edit', views.edit_subject),
	path('subjects/<int:subject_id>/update', views.update_subject),
	path('subjects/<int:subject_id>/delete', views.delete_subject),
	path('create_assignment/<int:subject_id>', views.create_assignment),
	path('login', views.user_login),
	path('logout',views.logout),
	path('inbox/<int:id>',views.inbox),
	path('send', views.send_message),
	path('message/<int:id>', views.open_message),
	path('new_message', views.new_message),
	path('delete_inbox_message/<int:id>', views.delete_inbox_message),
	path('delete_sent_message/<int:id>', views.delete_sent_message),
]