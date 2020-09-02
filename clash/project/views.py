from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Register,Response,Questions
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import re
import random
app_name='project'


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

que_id = [1,2,3,4,5,6,7,8,9,10]
def signin(request):
    global que_id
    if request.method=='POST':
        data=request.POST
        username=data['username']
        password=data['password']
        user=authenticate(request,username=username,password=password)

        if user:
            global que_id
            random.shuffle(que_id)
            login(request,user)

            return HttpResponseRedirect(reverse('success'))
        return render(request,'task2part2temp/signin.html',{'msg':['Invalid Credentials!']})
    return render(request,'task2part2temp/signin.html')


def success(request):

    getuser=Register.objects.get(user=request.user)

    if request.method=='POST':
        if not User.is_active:
            return render(request, 'task2part2temp/signin.html', {'msg': ['Already Played']})

        user_input=request.POST['user_ans']
        pre_question = Questions.objects.get(pk=que_id[getuser.que])

        if(pre_question.correct_answer==user_input):
            score=4
        else:
            score=-2
        respo=Response(question=pre_question, user=getuser.user, selected_answer=user_input, score=score)
        respo.save()
        getuser.total_score += respo.score
        print(getuser.total_score)
        getuser.que += 1

        getuser.save()
    if getuser.que == 10:
        return render (request,'task2part2temp/success.html',{'user':getuser,'msg':['Quiz Finished Attempted all the questions']})
    getuser=Register.objects.get(user=request.user)
    question=Questions.objects.get(pk=que_id[getuser.que])
    getuser.que+=1

    return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question})



def userlogout(request):
    logout(request)
    return render(request,'task2part2temp/signin.html',{'msg':['Logged Out Successfully ! Login/Signup Again']})
