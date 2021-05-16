from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, get_user_model, login

from users.forms import LoginForm, RegisterForm

UserModel = get_user_model()

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
    context = { 'form': RegisterForm() }
    if request.POST:
        post = request.POST

        if 'register' in post:
            form = RegisterForm(post)
            if form.is_valid():
                data = form.cleaned_data
                new_user = UserModel.objects.create(
                    name=data['name'],
                    last_name=data['last_name'],
                    nick=data['nick'],
                    email=data['email']
                )
                new_user.set_password(data['password'])
                new_user.save()
                return redirect('login')
            else:
                context['form'] = form

    return render(request, 'users/register.html', context)


def login_view(request: HttpRequest):
    context = { }

    if request.POST:
        post = request.POST

        if 'login' in post:
            form = LoginForm(post)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                email = cleaned_data.get('email')
                password = cleaned_data.get('password')
                user = authenticate(request, username=email, password=password)
                login(request, user)
                return redirect('home')
            else:
                context['form'] = form

    return render(request, 'users/login.html', context)