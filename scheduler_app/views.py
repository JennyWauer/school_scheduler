from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from .models import students
from .models import Subject
from .models import Assignment
from .models import inbox_messages
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

def logout(request):
	request.session.flush()
	return redirect('/')

def profile(request):
    if 'user_id' in request.session:
        user = Users.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'subjects':Subject.objects.all(),

            }
            return render(request, 'profile.html', context)
    return redirect('/')

def subject_page(request, subject_id):
    if 'user_id' in request.session:
        user = Users.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'subject': Subject.objects.get(id=subject_id),
                'assignments':Assignment.objects.all(),
				'subject_id': subject_id

            }
            return render(request, 'class_page.html', context)
    return redirect('/')


def edit_subject(request, subject_id):
    if 'user_id' in request.session:
        user = Users.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
				'subjects': Subject.objects.all(),
                'edit_subject': Subject.objects.get(id=subject_id),
            }
            return render(request, 'profile.html', context)
    return redirect('/')


def inbox(request, id):
	user = Users.objects.get(id=request.session['user_id'])
	context = {
		'user': user,
		'messages': inbox_messages.objects.all(),
		'all_users': Users.objects.all(),
	}
	return render(request, 'inbox.html', context)

def open_message(request, id):
	user = Users.objects.get(id=request.session['user_id'])
	message = inbox_messages.objects.get(id=id)
	context = {
		'user': user,
		'message': message,
	}
	return render(request, 'opened_message.html', context)

def new_message(request):
	user = Users.objects.get(id=request.session['user_id'])
	context = {
		'user': user,
		'messages': inbox_messages.objects.all(),
		'all_users': Users.objects.all(),
	}
	return render(request, 'new_message.html', context)

#<---------POST METHODS------>

#REGISTER METHOD
def create_user(request):
	print(" Can I create a user?!")
	if request.method != "POST":
		return redirect('/')
	errors = Users.objects.validate(request.POST)
		#if the dictionary received has errors in it, reject the form, and show the error messages
		# on the template the user was on last
	if len(errors) > 0:
		print(errors)
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/')
	else:
		user_pw=request.POST['password']
		# create the hash for the password
		hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
		print(hash_pw)
		# create user object 
		new_user = Users.objects.create(
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
		logged_user=Users.objects.filter(email=request.POST['email'])

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
				return redirect ('/register')
		else:
			messages.error(request, "Your email does not exist.")
			return redirect ('/register')
	return redirect('/profile')

#INBOX METHOD
def send_message(request):
	new_message = inbox_messages.objects.create(
        subject = request.POST['subject'],
		message = request.POST['message'],
		sender = Users.objects.get(id=request.session['user_id']),
        recipient = Users.objects.get(id=request.POST['recipient']),
    )
	return redirect('/profile')

def delete_inbox_message(request, id):
	destroyed = inbox_messages.objects.get(id=id)
	user = Users.objects.get(id=request.session['user_id'])
	if destroyed.recipient == user:
		destroyed.delete()
	return redirect('/profile')

def delete_sent_message(request, id):
	destroyed = inbox_messages.objects.get(id=id)
	user = Users.objects.get(id=request.session['user_id'])
	if destroyed.sender == user:
		destroyed.delete()
	return redirect('/profile')

#SUBJECT METHOD
def create_subject(request):
    errors = Subject.objects.subject_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/profile')
    else:
        user = Users.objects.get(id=request.session['user_id'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        subject = Subject.objects.create(
            name=request.POST['name'],
            url=request.POST['url'],
            lecture_date=request.POST['lecture_date'],
            description=request.POST['description'],
            teacher=user
        )
        
        return redirect('/profile')
    return redirect("/")


def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return redirect('/profile')


def update_subject(request, subject_id):
    if request.method=='POST':
        errors = Subject.objects.subject_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/subjects/{subject_id}/edit')
        my_subject=Subject.objects.get(id=subject_id)
        my_subject.name=request.POST['new_name']
        my_subject.url=request.POST['new_url']
        my_subject.lecture_date=request.POST['new_lecture_date']
        my_subject.description=request.POST['new_description']
        my_subject.save()

    return redirect(f'/subject/{subject_id}')


def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return redirect('/profile')


def create_assignment(request, subject_id):
    errors = Assignment.objects.assignment_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/subject_page')
    print('have we gotten this far?')
    print(subject_id)
    user = Users.objects.get(id=request.session['user_id'])
    subject = Subject.objects.get(id=subject_id)
    assignment = Assignment.objects.create(
        title=request.POST['title'],
        due_date=request.POST['due_date'],
        description=request.POST['description'],
        teacher=user,
        subject=subject

        )
        
    return redirect(f'/subjects/{subject.id}')


def delete_assignment(request, assignment_id):
    subject = Subject.objects.get(id=subject_id)
    assignment = Assignment.objects.get(id=assignment_id)
    assignment.delete()
    return redirect(f'/subjects/{subject.id}')


