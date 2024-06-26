from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import update_session_auth_hash
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "중복된 E-mail입니다.")
                return render(request, 'accounts/signup.html', {'form': form})
            else:
                user = form.save()
                auth_login(request, user)
                return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next') or 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('index')


@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            New_password = form.cleaned_data.get("New password")
            if User.objects.filter(password=New_password).exists:
                messages.error(request, '이전 비밀번호와 같은 비밀번호로 설정할 수 없습니다.')
                return render(request, 'accounts/change_password.html', {'form': form})
            else:
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)
