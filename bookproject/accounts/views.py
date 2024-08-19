from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile

def show_account(request):
    context = {}
    if request.POST and 'register' in request.POST:
        context['register'] = True
        try:
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            print(request.POST)

            # Create user account
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Create user profile with default role 'user'
            userprofile = UserProfile.objects.create(
                user=user,
                name=name,
                phone=phone,
                address=address,
                role='user'  # default role
            )
            success_message = "Registration successful"
            messages.success(request, success_message)
        except Exception as e:
            error_message = "Duplicate username or invalid input"
            messages.error(request, error_message)
    elif request.POST and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            user_profile = user.user_profile
            if user_profile.role == 'admin':
                return redirect('booklist')
            elif user_profile.role == 'user':
                return redirect('user_view')
        else:
            messages.error(request, 'Invalid user credentials')
    return render(request, 'account.html', context)

def sign_out(request):
    logout(request)
    return redirect('account')