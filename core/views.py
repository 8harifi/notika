from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.forms import CustomSignupForm

def landin_view(request):
    return render(request, "landing.html")


@login_required
def search_results_view(request):
    return render(request, "search_results.html")


@login_required
def search_view(request):
    return render(request, "search.html")


@login_required
def favorites_view(request):
    return render(request, "favorites.html")


@login_required
def upload_view(request):
    return render(request, "upload.html")


class SignupView(CreateView):
    form_class = CustomSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('core:landing')  # or wherever you want

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

