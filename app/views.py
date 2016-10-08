# from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "index.html", context)

def owner_profile(request):
    context = {}
    return render(request, "owner_profile.html", context)


def owner_profile_edit(request):
    context = {}
    return render(request, "owner_profile_edit.html", context)


def renter_profile(request):
    context = {}
    return render(request, "renter_profile.html", context)


def renter_profile_edit(request):
    context = {}
    return render(request, "renter_profile_edit.html", context)


def car(request):
    context = {}
    return render(request, "car.html", context)


def car_edit(request):
    context = {}
    return render(request, "car_edit.html", context)

def car_list(request):
    context = {}
    return render(request, "car_list.html", context)

def transaction(request):
    context = {}
    return render(request, "transaction.html", context)

#     auth

def login(request):
    context = {}
    return render(request, "auth/login.html", context)

def registration(request):
    context = {}
    return render(request, "auth/registration.html", context)

def forgot_password(request):
    context = {}
    return render(request, "auth/forgot_password.html", context)
