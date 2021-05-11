from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, get_user_model, login, logout
import re

User = get_user_model()

# Create your views here.
def start_view(request: HttpRequest):
    if request.POST:
        post = request.POST
        if 'login' in post:
            return redirect('login')
        elif 'register' in post:
            return redirect('register')
    return render(request, 'users/start.html')


def register_view(request: HttpRequest):
    context = { }
    if request.POST:
        post = request.POST
        if 'register' in post:
            context['name'] = post['name']
            name = post['name']
            if name == '':
                context['name_error_msg'] = 'Name required'

            context['last_name'] = post['last_name']
            last_name = post['last_name']

            context['nick'] = post['nick']
            nick = post['nick']
            if nick == '':
                context['nick_error_msg'] = 'Nick required'
            else:
                by_nick = User.objects.filter(nick=nick)
                if by_nick:
                    context['nick_error_msg'] = 'Nick already taken'


            context['email'] = post['email']
            email = post['email']
            if email == '':
                context['email_error_msg'] = 'Email required'
            elif User.objects.filter(email=email):
                context['email_error_msg'] = 'Email already taken'
            elif not re.match('.+@.+\..+', email):
                context['email_error_msg'] = 'Enter a valid email'

            password = post['password']
            password_conf = post['password_conf']
            if password == '':
                context['pass_error_msg'] = 'Password required'
            elif password != password_conf:
                context['pass_conf_error_msg'] = 'Passwords don\'t match'

        error = 'name_error_msg' in context or \
                'nick_error_msg' in context or \
                'email_error_msg' in context or \
                'pass_error_msg' in context or \
                'pass_conf_error_msg' in context

        if not error:
            UserModel = get_user_model()
            new_user: User = UserModel.objects.create(
                name=name,
                last_name=last_name,
                nick=nick,
                email=email
            )
            new_user.set_password(password)
            new_user.save()
            print(new_user)
            return redirect('login')

    return render(request, 'users/register.html', context)


def login_view(request: HttpRequest):
    context = {
        'error': False,
        'error_message': '',
    }

    if request.POST:
        post = request.POST
        if 'login' in post:
            email = post['email']
            password = post['password']

            user: User = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context['error'] = True
                context['error_message'] = 'Invalid email and password combination'


    print(request.POST)
    print(context)
    return render(request, 'users/login.html', context)