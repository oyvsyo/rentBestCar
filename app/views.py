# from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html", {"test": "test2"})


def owner_profile(request):
    return render(request, "index.html", {"test": "test2"})


def owner_profile_edit(request):
    return render(request, "index.html", {"test": "test2"})


def renter_profile(request):
    return render(request, "index.html", {"test": "test2"})


def renter_profile_edit(request):
    return render(request, "index.html", {"test": "test2"})
