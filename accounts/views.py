from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, )
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileImageForm


# 로그인
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or "products:product_list"
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    context = {"form": form}
    return render(request, "login.html", context)


# 로그아웃
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("products:product_list")


# 사용자 업데이트
@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:update")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "update.html", context)


# 패스워드 변경
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:update")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "change_password.html", context)


# 회원가입
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 프로필 생성
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect("products:product_list")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "signup.html", context)


def users(request):
    return render(request, "users/users.html")


@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", username=member.username)
    return redirect("accounts:login")


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect("products:product_list")


# Create your views here.
@login_required
def profile(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user_id=user_id)
    else:
        form = ProfileImageForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'profile.html', context)


@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), pk=user_id)

        # Profile이 없으면 생성
        profile, created = Profile.objects.get_or_create(user=user)

        if user != request.user:
            if profile.followers.filter(pk=request.user.pk).exists():
                profile.followers.remove(request.user)
            else:
                profile.followers.add(request.user)

        return redirect('accounts:profile', user_id=user_id)

    return redirect('accounts:login')
