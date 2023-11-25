from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from user.forms import RegistrationForm, UserUpdateForm
from user.models import User

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This should trigger the User model's save method
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home_view')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Assuming email is used as the username field
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {user.username}')
                return redirect('home_view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def user_profile_view(request):
    return render(request, 'user_profile.html')

@login_required
def user_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # This should trigger the User model's save method
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile_view')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user_profile.html', {'form': form})
