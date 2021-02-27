from django.db import models
import re
import bcrypt
from datetime import datetime

class UsersManager(models.Manager):
    def validate(self, form):
        errors = {}
        if form['first_name'] == 'first_name':
            if len(form['value']) < 2:
                errors['first_name'] = "First name must be at least 2 characters"
        if form['last_name'] == 'last_name':
            if len(form['value']) < 2:
                errors['last_name'] = "Last name must be at least 2 characters"
        if form['email'] == 'email':
            if not EMAIL_REGEX.match(form['email']):            
                errors['email'] = ("Invalid email address!")
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if form['password'] == 'password' and len(form['value']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
    def __repr__(self):
        return f"<ID: ({self.id}) \nName:{self.first_name} {self.last_name}>"


class studentsManager(models.Manager):
    def validate(self, form):
        errors = {}
        if form['fieldName'] == 'first_name':
            if len(form['value']) < 2:
                errors['first_name'] = "First name must be at least 2 characters"
        if form['fieldName'] == 'last_name':
            if len(form['value']) < 2:
                errors['fieldName'] = "Last name must be at least 2 characters"
        return errors

class students(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	user = models.ManyToManyField(Users, related_name="user_students")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = studentsManager()
	def __repr__(self):
		return f"<ID: ({self.id}) \nName:{self.first_name} {self.last_name}>"


class subjectManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['name']) < 3:
            errors['name'] = "Subject name must be at least 3 characters"
        if len(form['description']) < 10:
            errors['description'] = "Description must be at least 10 characters"
        if len(form['url']) < 10:
            errors['url'] = "Description must be at least 10 characters"
        if datetime.strptime(form['lecture_date'], '%Y-%m-%d') <= datetime.now():
            errors["trip_start"] = "Lecture date cannot be in the past"
        return errors

class subjects(models.Model):
	name = models.CharField(max_length=45)
	url = models.TextField()
	lecture_date = models.DateTimeField()
	description = models.TextField()
	teacher = models.ForeignKey(Users, related_name="teacher_subjects",on_delete = models.CASCADE)
	enrolled_students = models.ManyToManyField(students, related_name="enrolled_subjects")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = subjectManager()
	def repr(self):
		return f"<ID: ({self.id}) \nName:{self.name}>"


class assignmentsManager(models.Manager):
	def validate(self, form):
		errors = {}
		if len(form['title']) < 3:
			errors['title'] = "Title must be at least 3 characters"
		if len(form['description']) < 10:
			errors['description'] = "Description must be at least 10 characters"
		if datetime.strptime(form['due_date'], '%Y-%m-%d') <= datetime.now():
			errors["trip_start"] = "Due date cannot be in the past"
		return errors

class assignments(models.Model):
	title = models.CharField(max_length=45)
	subject = models.ForeignKey(subjects, related_name="subject_assignments",on_delete = models.CASCADE)
	description = models.TextField()
	due_date = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = assignmentsManager()
	def repr(self):
		return f"<ID: ({self.id}) \nTitle:{self.title}>"


class messagesManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['subject']) < 0:
            errors['subject'] = "Subject field cannon be empty"
        if len(form['message']) < 0:
            errors['description'] = "Message field cannot be empty"
        return errors

class messages(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(Users, related_name="sent_messages",on_delete = models.CASCADE)
    recipient = models.ForeignKey(Users, related_name="received_messages",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
