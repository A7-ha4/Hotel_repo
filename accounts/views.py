from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def auth_view(request):
    login_form = LoginForm(request, data=request.POST or None)
    register_form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if 'login' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials.")
                return redirect('register')

    return render(request, 'login.html', {
        'login_form': login_form,
        'register_form': register_form,
    })


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to dashboard or home page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


