from django.shortcuts import render, redirect, HttpResponse
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Register, Response, Questions
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import re
import random
import datetime
from django.utils import timezone
from django.views.decorators.cache import cache_control

app_name = 'project'
number_of_questions = 12


def check(request):
    username_lst = []
    user_list = User.objects.values()
    for user in user_list:
        username_lst.append(user['username'])
    data = {'is_taken': False}
    if request.GET.get('name') in username_lst:
        data = {'is_taken': True}

    return JsonResponse(data)


def signup(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('success')
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        conf_pass = data['confirm_password']
        level = data['level']
        language = data['language']
        regexusername = "^[[A-Z]|[a-z]][[A-Z]|[a-z]|\\d|[_]]{7,29}$"
        regexemail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regexusername, username):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Username is Not Valid"]})
        if not re.search(regexemail, email):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Email ID is not Valid"]})
        if not str(firstname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["First Name is not Valid"]})
        if not str(lastname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["Last Name is not Valid"]})
        if not str(phone).isnumeric() and len(phone) == 10 and phone < 59999999999:
            return render(request, 'task2part2temp/signup.html', {'msg': ["Invalid Phone Number is Entered"]})
        if password != conf_pass:
            return render(request, 'task2part2temp/signup.html', {'msg': ["Passwords Don't match"]})
        try:
            ouruser = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email,
                                               password=password)
            newuser = Register(user=ouruser, phone=phone, level=level, language=language)
            ouruser.save()
            newuser.save()
            newuser.status = False
            newuser.save()
            lst = []
            for i in range(0, 10):
                while True:
                    questionNo = random.randint(1, 12)
                    if questionNo not in lst:
                        break
                lst.append(questionNo)
            newuser.cq = lst[-1]
            newuser.quelist = json.dumps(lst)
            auth.login(request, ouruser)
            newuser.save()
            return HttpResponseRedirect(reverse('success'))
            # return HttpResponse("creartedpython manage")
        except:
            return render(request, 'task2part2temp/signup.html', {'msg': ["User already exists"]})
    return render(request, 'task2part2temp/signup.html')


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)


def signin(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        try:
            getuser = Register.objects.get(user=user)
            if user and getuser.status == True:
                login(request, user)
                getuser.status = False
                getuser.save()
                return HttpResponseRedirect(reverse('success'))
            return render(request, 'task2part2temp/signin.html', {'msg': ['Invalid Credentials!'], 'user': getuser})
        except:
            return render(request, 'task2part2temp/signin.html', {'msg': ['Invalid Credentials!']})
    return render(request, 'task2part2temp/signin.html')


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
def success(request):
    try:
        getuser = Register.objects.get(user=request.user)
        time_diff = timezone.now() - request.user.last_login
        time_rem = datetime.timedelta(minutes=28) - time_diff
        total_seconds = time_rem.total_seconds()
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        if total_seconds <= 0:
            return redirect('logout')
        msg2 = "TIME REMAINING  = " + str(minutes) + ":" + str(seconds)
        lst = json.loads(getuser.quelist)
        if request.method == 'GET' and getuser.user.is_authenticated:
            pass
        if request.method == 'POST':
            if request.POST.get('submit') == str(lst[-1]):
                user_input = request.POST['user_ans']
                pre_question = Questions.objects.get(pk=lst[-1])
                if getuser.bool == True:
                    if pre_question.correct_answer == user_input:
                        score = 4
                        bool = True
                    else:
                        score = -2
                        bool = False
                else:
                    if pre_question.correct_answer == user_input:
                        score = 2
                        bool = True
                    else:
                        score = -1
                        bool = False

                respo = Response(question=pre_question, user=getuser.user, selected_answer=user_input, score=score)
                respo.save()
                getuser.total_score += respo.score
                lst.pop()
                getuser.bool = bool
                getuser.save()

        if len(lst) == 0:
            return HttpResponseRedirect(reverse('logout'))
        question = Questions.objects.get(pk=lst[-1])
        getuser.quelist = json.dumps(lst)
        getuser.save()
        return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question, 'time': [msg2]})
    except:
        return render(request, 'task2part2temp/signin.html', {'msg': ['Login First ..!!']})
    return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question, 'time': [msg2]})
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)


def userlogout(request):
    try:
        getuser = Register.objects.get(user=request.user)
        getuser.logouttime = timezone.now()
        getuser.save()
        logout(request)
        return render(request, 'task2part2temp/result.html', {'user': getuser, 'msg': ['Quiz Finished']})
    except:
        return render(request, 'task2part2temp/signup.html', {'msg': ['You need To Login/Register First :)']})
