# from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    return JsonResponse({'You are welcome to ': 'RENTBESTCAR 1.0'})

