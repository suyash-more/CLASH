from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Register,Response,Questions
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import re
import random
app_name='project'
number_of_questions=12


def signup(request):
    if request.method=='POST':
        data=request.POST
        username=data['username']
        firstname=data['firstname']
        lastname=data['lastname']
        email=data['email']
        phone=data['phone']
        password=data['password']
        conf_pass=data['confirm_password']
        level=data['level']
        language=data['language']
        regexusername = "^[[A-Z]|[a-z]][[A-Z]|[a-z]|\\d|[_]]{7,29}$"
        regexemail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regexusername,username):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Username is Not Valid"]})
        if not re.search(regexemail,email):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Email ID is not Valid"]})
        if not str(firstname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["First Name is not Valid"]})
        if not str(lastname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["Last Name is not Valid"]})
        if not str(phone).isnumeric() and len(phone)==10 and phone<59999999999:
            return render(request, 'task2part2temp/signup.html', {'msg': ["Invalid Phone Number is Entered"]})
        if password!=conf_pass:
            return render(request,'task2part2temp/signup.html',{'msg': ["Passwords Don't match"]})
        try:
            ouruser=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
            newuser = Register(user=ouruser,phone=phone,level=level,language=language)
            ouruser.save()
            newuser.save()
            auth.login(request,ouruser)
            return render(request, 'task2part2temp/signup.html', {'msg': ["User Registered"]})
        except:
            return render(request, 'task2part2temp/signup.html', {'msg': ["User already exists"]})
    return render(request,'task2part2temp/signup.html')



def signin(request):
    if request.method=='POST':
        data=request.POST
        username=data['username']
        password=data['password']
        user=authenticate(request,username=username,password=password)
        getuser = Register.objects.get(user=user)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('success'))
        return render(request,'task2part2temp/signin.html',{'msg':['Invalid Credentials!']})
    return render(request,'task2part2temp/signin.html')


def success(request):
    getuser=Register.objects.get(user=request.user)
    lst=json.loads(getuser.quelist)
    if request.method=='GET':
        questionNo = random.randint(1, 12)
        lst.append(questionNo)
    if request.method=='POST':
        while True:
            questionNo = random.randint(1,12)
            if questionNo not in lst:
                break
        lst.append(questionNo)
        user_input=request.POST['user_ans']
        pre_question = Questions.objects.get(pk=lst[-2])
        if pre_question.correct_answer==user_input:
            score=4
        else:
            score=-2
        respo=Response(question=pre_question, user=getuser.user, selected_answer=user_input, score=score)
        respo.save()
        getuser.total_score += respo.score
        print(getuser.total_score)
        getuser.save()
    if len(lst) == 10:
        return render(request,'task2part2temp/success.html',{'user':getuser,'msg':['Quiz Finished Attempted all the questions']})
    question=Questions.objects.get(pk=questionNo)
    getuser.quelist=json.dumps(lst)
    getuser.save()
    return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question})




def userlogout(request):
    logout(request)
    return render(request,'task2part2temp/signin.html',{'msg':['Logged Out Successfully ! Login/Signup Again']})
