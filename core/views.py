from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def search_results_view(request):
    return render(request, "search_results.html")




