from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager,StudentManager, Student,SubjectManager,Subject, AssignmentManager, Assignment, MessageManager, Message
from django.contrib import messages
import bcrypt
# Create your views here.

#GET
def index(request):
	return render(request, 'index.html')

def login_reg(request):
	return render(request, 'login_reg.html')

def add_user(request):
	return render(request, 'login_reg.html')


def roster_list(request, subject_id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            request.session['subject_id'] = subject_id
            context = {
                'user': user[0],
                'mysubjects':Subject.objects.get(id=subject_id),
				'class_students':Student.objects.filter(enrolled_subjects=subject_id),
                'non_class_students':Student.objects.exclude(enrolled_subjects=subject_id),
            }
            return render(request, 'roster.html', context)
    return redirect('/')

def logout(request):
	request.session.flush()
	return redirect('/')

def profile(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'subjects':Subject.objects.all(),

            }
            return render(request, 'profile.html', context)
    return redirect('/')

def subject_page(request, subject_id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            print("Testing")
            request.session['subject_id'] = subject_id
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
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'edit_subject': Subject.objects.get(id=subject_id),
            }
            return render(request, 'edit_subject.html', context)
    return redirect('/')

def all_classes(request):
	context = {
		"all_student": Student.objects.all(),
        "all_subjects":Subject.objects.all(),
        "teacher":User.objects.all(),
        "student_assignment":Assignment.objects.all()

	}
	return render(request, 'all_classes.html', context)

def edit_assignment(request, assignment_id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'edit_assignment': Assignment.objects.get(id=assignment_id),
            }
            return render(request, 'edit_assignment.html', context)
    return redirect('/')

def student_assign(request, student_id):
	context = {
		'myassignments': Assignment.objects.filter(id=student_id),
		"teacher" : User.objects.all(),
		"this_student":Student.objects.get(id=student_id),
		"mysubjects": Subject.objects.filter(enrolled_students=student_id)
	}
	return render(request, 'student_page.html', context)

def class_profile(request):
	context = {
		"user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'profile.html',context)

def logout(request):
	request.session.flush()
	return redirect('/')

def inbox(request, id):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user': user,
		'messages': Message.objects.all(),
		'all_users': User.objects.all(),
	}
	return render(request, 'inbox.html', context)

def open_message(request, id):
	user = User.objects.get(id=request.session['user_id'])
	message = Message.objects.get(id=id)
	context = {
		'user': user,
		'message': message,
	}
	return render(request, 'opened_message.html', context)

def new_message(request):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user': user,
		'messages': Message.objects.all(),
		'all_users': User.objects.all(),
	}
	return render(request, 'new_message.html', context)

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
	
		print('Checking User Role 2')
		if new_user.role == "2":
			#return redirect('/parent')
			return redirect(f"/parent/{new_user.id}")
		else:
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
				
				print('Checking User Role 2')
				if logged_user.role == "2":
					#return redirect('/parent')
					return redirect(f"/parent/{logged_user.id}")
				else:
					return redirect('/profile')
			else :
				messages.error(request, "Your password is incorrect.")
				return redirect ('/register')
		else:
			messages.error(request, "Your email does not exist.")
			return redirect ('/register')
		
		print('Checking User Role 2')
		if logged_user.role == "2":
			#return redirect('/parent')
			return redirect(f"/parent/{logged_user.id}")
		else:
			return redirect('/profile')



def add_student(request):
    print('Can I add a student to the db? ')
    if request.method == "POST":
        error = Student.objects.validate(request.POST)
        if error:
            messages.error(request, error)
            return redirect ('/all_classes')
        this_user = User.objects.get(id=request.session['user_id'])
        add_new_student = Student.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
        )
        # add student to user = i.e. to teacher who is logged in [user_id]
        add_new_student.user.add(this_user)
        subject_id=request.session['subject_id'] 
    return redirect (f'roster/{subject_id}')



def delete_sent_message(request, id):
	destroyed = Message.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	if destroyed.sender == user:
		destroyed.delete()
	return redirect('/profile')

#SUBJECT METHOD
def create_subject(request):
    errors = Subject.objects.validate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/profile')
    else:
        user = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        subject = Subject.objects.create(
            name=request.POST['name'],
            url=request.POST['url'],
            lecture_date=request.POST['lecture_date'],
            description=request.POST['description'],
            teacher=user
        )
        request.session['subject_id'] = subject.id
        return redirect('/profile')
    return redirect("/")


def update_subject(request, subject_id):
    if request.method=='POST':
        errors = Subject.objects.validate_update(request.POST)
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

    return redirect(f'/profile')


def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return redirect('/profile')


def create_assignment(request, subject_id):
	errors = Assignment.objects.validate(request.POST)

	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/subject_page')
	print('have we gotten this far?')
	print(subject_id)
	user = User.objects.get(id=request.session['user_id'])
	subject = Subject.objects.get(id=subject_id)
	print('trying to create an assignment?')
	print('request title', request.POST['title'])
	print('request due date', request.POST['due_date'])
	print('request desc', request.POST['description'])
	assignment = Assignment.objects.create(
		title=request.POST['title'],
		due_date=request.POST['due_date'],
		description=request.POST['description'],
		teacher = user,
		subject=subject    
		)
	return redirect(f'/subjects/{subject.id}')

def update_assignment(request, assignment_id):
    if request.method=='POST':
        errors = Subject.objects.validate_update(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/subjects/{subject_id}/edit')
        my_assignment=Assignment.objects.get(id=assignment_id)
        my_assignment.title=request.POST['new_title']
        my_assignment.due_date=request.POST['new_due_date']
        my_assignment.description=request.POST['new_description']
        my_assignment.save()

    return redirect(f'/subjects/{subject.id}')


# def assignparent(request, student_id):
# 	if 'user_id' in request.session:  #Is the user logged in
# 		user = User.objects.get(id=request.session['user_id']) #create instance of user to add to student
# 		studenttoassign =  Student.objects.get(id=student_id) #create instance of student to assign parent
# 		studenttoassign.user.add(user) #Many to many we add
# 		studenttoassign.save()

# 	return redirect(f"/parent/{user.id}")


def delete_assignment(request, assignment_id):
    subject=Subject.objects.get(id=request.session['subject_id'])
    assignment = Assignment.objects.get(id=assignment_id)
    assignment.delete()
    return redirect(f'/subjects/{subject.id}')


def delete_student (request, student_id):
	print("I want to delete a student!")
	delete_student=Student.objects.get(id=student_id)
	delete_student.delete()
	return redirect ('/all_classes')

#Parent Functions
def parent(request, user_id):
    if 'user_id' in request.session:  #Is the user logged in

        this_user = User.objects.filter(id=request.session['user_id']),
        context = {
                'user': User.objects.get(id=request.session['user_id']), #create instance of user to add to record
                #'allstudents': Student.objects.all(), #All students
				'mystudents': Student.objects.filter(user=user_id), #Grab Only User students
				'notmystudents': Student.objects.exclude(user=user_id), #Grab Only User students
				#'subjects': Subject.objects.all(), #All subjects
            }
        return render(request,'parent.html', context) #if valid user than we move on to success
    return redirect("/login") #no matter what success handles the view and the session

def assignparent(request, student_id):
	if 'user_id' in request.session:  #Is the user logged in
		user = User.objects.get(id=request.session['user_id']) #create instance of user to add to student
		studenttoassign =  Student.objects.get(id=student_id) #create instance of student to assign parent
		studenttoassign.user.add(user) #Many to many we add
		studenttoassign.save()

	return redirect(f"/parent/{user.id}")


def viewstudent(request, student_id):
	context = {
		'myassignments': Assignment.objects.filter(id=student_id),
		# "assign": Assignment.objects.all(),
		"teacher" : User.objects.all(),
		"this_student":Student.objects.get(id=student_id)
	}
	return render(request, 'student_page.html', context)

#INBOX METHOD
def send_message(request):
	new_message = Message.objects.create(
        subject = request.POST['subject'],
		message = request.POST['message'],
		sender = User.objects.get(id=request.session['user_id']),
        recipient = User.objects.get(id=request.POST['recipient']),
    )
	return redirect('/profile')

def delete_inbox_message(request, id):
	destroyed = Message.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	if destroyed.recipient == user:
		destroyed.delete()
	return redirect('/profile')

def delete_sent_message(request, id):
	destroyed = Messages.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	if destroyed.sender == user:
		destroyed.delete()
	return redirect('/profile')

def roster_assign(request, student_id):
    if 'user_id' in request.session:  #Is the user logged in
        user = User.objects.get(id=request.session['user_id']) #create instance of user to add to student
        subject = Subject.objects.get(id=request.session['subject_id']) # gives us a specific instance of a subject
        studenttoassign =  Student.objects.get(id=student_id) #create instance of student to assign subject
        studenttoassign.enrolled_subjects.add(subject)
        # studenttoassign.user.add(user) #Many to many we add
        studenttoassign.save()
    return redirect(f"/roster/{subject.id}")


