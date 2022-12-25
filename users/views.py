from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm



def user_signup(request):
    
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created Successfully.')
            return redirect('login')

    return render(request, 'users/signup.html', context={'form': form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In successfully.')
            return redirect('register')
        else:
            messages.success(request, 'Invalid credentials.')
            return redirect('login')
    return render(request, 'users/login.html')



def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('login')