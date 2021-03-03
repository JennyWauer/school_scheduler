from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager,StudentManager, Student,SubjectManager,Subject, AssignmentManager, Assignment, MessageManager, Message
from django.contrib import messages
import bcrypt
# Create your views here.

#GET
def index(request):
	print("is this render request even working? ")
	return render(request, "index.html")

def index(request):
	return render(request, 'index.html')

def add_user(request):
	return render(request, 'login_reg.html')

def all_classes(request):
	context = {
		"all_student": Student.objects.all()
	}
	return render(request, 'all_classes.html', context)

def edit_assign(request):
	return render(request, 'edit_assignment.html')

def student_assign(request):
	context = {
		"assign": Assignment.objects.all(),
		"teacher" : User.objects.all(),
	}
	return render(request, 'student_page.html')

def class_profile(request):
	context = {
		"user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'profile.html',context)

def logout(request):
	request.session.flush()
	return redirect('/')


#<---------POST METHODS------>

#REGISTER METHOD
def create_user(request):
	print(" Can I create a user?!")
	if request.method != "POST":
		return redirect('/')
	errors = User.objects.validate(request.POST)
		#if the dictionary received has errors in it, reject the form, and show the error messages
		# on the template the user was on last
	if len(errors) > 0:
		print(errors)
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/register')
	else:
		user_pw=request.POST['password']
		# create the hash for the password
		hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
		print(hash_pw)
		# create user object 
		new_user = User.objects.create(
			first_name=request.POST['first_name'], 
			last_name=request.POST['last_name'], 
			email=request.POST['email'], 
			role = request.POST['role'],
			password=hash_pw,
		)
		print(new_user)
		# storing user's id so I can track user's interactions on the website 
		request.session['user_id']= new_user.id 
		request.session['first_name'] = new_user.first_name
		request.session['last_name'] = new_user.last_name
		request.session['role'] = new_user.role
	return redirect('/profile')

#LOGIN METHOD
def user_login(request):
	print('Is this user_login method working?')
	if request.method == 'POST':
		# query to find the user
		logged_user=User.objects.filter(email=request.POST['email'])

		if len(logged_user) > 0:
			logged_user = logged_user[0]
			print(logged_user)
			print(logged_user.password, request.POST['password'])

			if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
				request.session['user_id'] = logged_user.id 
				request.session['first_name'] = logged_user.first_name
				return redirect ('/profile')
			else :
				messages.error(request, "Your password is incorrect.")
				return redirect ('/')
		else:
			messages.error(request, "Your email does not exist.")
			return redirect ('/')
	return redirect('/profile')

#POST: Create / Add student
def add_student(request):
	print('Can I add a student to the db? ')
	if request.method == "POST":
		error = Student.objects.validate(request.POST)
		if error:
			messages.error(request, error)
			return redirect ('/all_classes')
		add_new_student = Student.objects.create(
			first_name = request.POST['first_name'],
			last_name = request.POST['last_name'],
		)
		user = User.objects.get(id=request.session['user_id'])
		#add student to user = ie teacher
		user.user_students.add(add_new_student)
	return redirect ('/all_classes')


def delete_student (request, student_id):
	print("I want to delete a student!")
	delete_student=Student.objects.get(id=student_id)
	delete_student.delete()
	return redirect ('/all_classes')
