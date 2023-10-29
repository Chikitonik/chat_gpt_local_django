from user_auth.models import UserProfile  # Import your UserProfile model
from .forms import EmailAuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, EmailAuthenticationForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)
            login(request, user)
            # Redirect to user profile
            return redirect('personal_page')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_auth_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Check if the user has a UserProfile
                user_profile, created = UserProfile.objects.get_or_create(
                    user=user)

                # Update the api_key in the UserProfile
                # user_profile.api_key = 'new_api_key'
                user_profile.save()

                # Redirect to the desired page after login
                return redirect('homepage')
            else:
                form.add_error(
                    None, "Invalid email or password. Please try again.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    # Log the user out
    logout(request)
    # Redirect to the homepage or any other desired URL
    return redirect('homepage')


def personal_page(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        user_profile.api_key = api_key
        user_profile.save()

    return render(request, 'personal_page.html', {'user_profile': user_profile})
