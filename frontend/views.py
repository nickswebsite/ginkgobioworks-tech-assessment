from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.conf import settings


def index(request):
    if request.user.is_authenticated:
        return redirect(
            static("index.html")
        )
    else:
        return redirect(settings.LOGIN_URL)
