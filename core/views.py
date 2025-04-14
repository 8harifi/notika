from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.forms import CustomSignupForm
from core.models import Favorite, Document
from django.db.models import Q

def landin_view(request):
    return render(request, "landing.html")


@login_required
def search_results_view(request):
    query = request.GET.get('q', '')
    results = Document.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(course__name__icontains=query)
    )
    return render(request, 'search_results.html', {'results': results, 'query': query})
    # return render(request, "search_results.html")


@login_required
def search_view(request):
    return render(request, "search.html")


@login_required
def favorites_view(request):
    user_id = request.user.id
    user_fav_items = [x.document for x in Favorite.objects.filter(user_id=user_id)]
    return render(request, "favorites.html", {'favorites': user_fav_items})


@login_required
def upload_view(request):
    return render(request, "upload.html")


@login_required
def edit_profile_view(request):
    return render(request, "profile.html")


class SignupView(CreateView):
    form_class = CustomSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('core:landing')  # or wherever you want

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

@login_required
def download_document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        return FileResponse(doc.file.open(), as_attachment=True, filename=doc.file.name)
    except Document.DoesNotExist:
        raise Http404("Document not found.")

