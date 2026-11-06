from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

from .web_forms import EmailLoginForm, RegisterForm

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("pickups:display_pickup_requests")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            role="requestor",
        )
        login(request, user)
        return redirect("pickups:display_pickup_requests")
    return render(request, "accounts/register.html", {
        "form": form,
        "page_label": "GET STARTED",
        "page_title": "Create requestor account",
        "page_description": "Request waste collection and track every pickup.",
        "submit_label": "Create account",
    })


def web_login(request):
    if request.user.is_authenticated:
        return redirect("pickups:display_pickup_requests")
    form = EmailLoginForm(request.POST or None, request=request)
    if request.method == "POST" and form.is_valid():
        login(request, form.user)
        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        if form.user.role == "admin" or form.user.is_superuser:
            return redirect("pickups:dashboard")
        return redirect("pickups:display_pickup_requests")
    return render(request, "accounts/login.html", {
        "form": form,
        "page_label": "WELCOME BACK",
        "page_title": "Sign in",
        "page_description": "Manage your waste collection service from one place.",
        "submit_label": "Sign in",
    })


@login_required
@require_POST
def web_logout(request):
    logout(request)
    return redirect("web_login")
