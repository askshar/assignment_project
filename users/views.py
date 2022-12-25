from django.shortcuts import render, redirect
from django.contrib import messages
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
    pass



def user_logout(request):
    pass