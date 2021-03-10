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
	path('assignments/<int:assignment_id>/edit',views.edit_assignment),
	path('assignments/<int:assignment_id>/update', views.update_assignment),
	path('assignments/<int:assignment_id>/delete', views.delete_assignment),
	path('cancel_edit', views.cancel_edit), 
	path('login', views.user_login),
	path('all_classes',views.all_classes),
	path('add_student',views.add_student),
	path('student_assign/<int:student_id>',views.student_assign),
	path('delete/<int:student_id>',views.delete_student),
	path('logout',views.logout),
	path('inbox/<int:id>',views.inbox),
	path('send', views.send_message),
	path('message/<int:id>', views.open_message),
	path('new_message', views.new_message),
	path('parent/<int:user_id>',views.parent),
	path('assignparent/<int:student_id>', views.assignparent),
	path('viewstudent/<int:student_id>', views.viewstudent),
	path('roster/<int:subject_id>',views.roster_list),
	path('assign_subject/<int:student_id>',views.roster_assign),
	path('delete_inbox_message/<int:id>', views.delete_inbox_message),
	path('delete_sent_message/<int:id>', views.delete_sent_message),
	path('login_reg', views.login_reg),
	path('all_classes', views.all_classes),
	path('go_to_subject',views.go_back_to_subject_page),
]