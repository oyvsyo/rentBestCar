# from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html", {"test": "test2"})
