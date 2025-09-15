from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from core.forms import CustomSignupForm, ProfileForm
from core.models import Favorite, Document, Course, Download
from django.db.models import Q, F
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
import os

def landin_view(request):
    if request.user.is_authenticated:
        return redirect('core:search')
    return render(request, "landing.html")


@login_required
def search_results_view(request):
    query = request.GET.get('q', '')
    results = Document.objects.select_related('course').filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(course__name__icontains=query)
    )
    doc_ids = list(results.values_list('id', flat=True))
    favorite_ids = set(Favorite.objects.filter(user=request.user, document_id__in=doc_ids).values_list('document_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'search_results.html', {'results': results, 'query': query, 'favorite_ids': favorite_ids})
    # return render(request, "search_results.html")


@login_required
def search_view(request):
    return render(request, "search.html")


@login_required
def favorites_view(request):
    user_id = request.user.id
    user_fav_items = [x.document for x in Favorite.objects.filter(user_id=user_id)]
    favorite_ids = set(doc.id for doc in user_fav_items)
    return render(request, "favorites.html", {'favorites': user_fav_items, 'favorite_ids': favorite_ids})


@login_required
def upload_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        course_id = request.POST.get("course_id")
        upload_file = request.FILES.get("file")

        if title and course_id and upload_file:
            try:
                course = Course.objects.get(id=course_id)
                Document.objects.create(
                    title=title,
                    description=description,
                    file_path=upload_file,
                    uploaded_by=request.user,
                    course=course,
                )
                return redirect("core:upload")
            except Course.DoesNotExist:
                pass

    courses = Course.objects.all().order_by("name")
    recent_docs = Document.objects.select_related('course').filter(uploaded_by=request.user).order_by("-upload_date")[:24]
    fav_ids = set(Favorite.objects.filter(user=request.user, document_id__in=list(recent_docs.values_list('id', flat=True))).values_list('document_id', flat=True))
    return render(request, "upload.html", {"courses": courses, "recent_docs": recent_docs, "favorite_ids": fav_ids})


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, user=request.user, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get("new_password")
            if new_password:
                user.set_password(new_password)
            user.save()
            # If password changed, re-login to keep session
            if new_password:
                login(request, user)
            return redirect("core:edit_profile")
    else:
        form = ProfileForm(user=request.user, instance=request.user)
    return render(request, "profile.html", {"form": form})


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
        # Record download and increment counter
        Download.objects.create(user=request.user, document=doc, ip=request.META.get("REMOTE_ADDR", "0.0.0.0"))
        Document.objects.filter(id=doc.id).update(downloads=F('downloads') + 1)  # atomic increment

        return FileResponse(
            doc.file_path.open("rb"),
            as_attachment=True,
            filename=doc.file_path.name.split("/", 1)[-1],
        )
    except Document.DoesNotExist:
        raise Http404("Document not found.")


@require_POST
@login_required
def add_favorite(request):
    doc_id = request.POST.get("doc_id")
    if not doc_id:
        return JsonResponse({"success": False, "error": "Missing doc_id"}, status=400)
    try:
        doc = Document.objects.get(id=doc_id)
        _, created = Favorite.objects.get_or_create(user=request.user, document=doc)
        return JsonResponse({"success": True, "created": created})
    except Document.DoesNotExist:
        return JsonResponse({"success": False, "error": "Document not found"}, status=404)


@require_POST
@login_required
def toggle_favorite(request):
    doc_id = request.POST.get("doc_id")
    if not doc_id:
        return JsonResponse({"success": False, "error": "Missing doc_id"}, status=400)
    try:
        doc = Document.objects.get(id=doc_id)
        fav = Favorite.objects.filter(user=request.user, document=doc)
        if fav.exists():
            fav.delete()
            return JsonResponse({"success": True, "is_favorite": False})
        Favorite.objects.create(user=request.user, document=doc)
        return JsonResponse({"success": True, "is_favorite": True})
    except Document.DoesNotExist:
        return JsonResponse({"success": False, "error": "Document not found"}, status=404)


@require_GET
@login_required
def document_info(request, doc_id):
    try:
        doc = Document.objects.select_related('course', 'uploaded_by').get(id=doc_id)
        file_name = doc.file_path.name if doc.file_path else ""
        ext = os.path.splitext(file_name)[1].lstrip('.') if file_name else ""
        size = doc.file_path.size if doc.file_path else 0
        is_favorite = Favorite.objects.filter(user=request.user, document=doc).exists()
        return JsonResponse({
            'id': doc.id,
            'title': doc.title,
            'description': doc.description,
            'course': doc.course.name if doc.course_id else None,
            'uploaded_by': getattr(doc.uploaded_by, 'username', None),
            'file_name': os.path.basename(file_name) if file_name else "",
            'extension': ext,
            'size': size,
            'downloads': doc.downloads,
            'views': doc.views,
            'is_favorite': is_favorite,
            'download_url': request.build_absolute_uri(reverse_lazy('core:download', kwargs={'doc_id': doc.id}))
        })
    except Document.DoesNotExist:
        return JsonResponse({"success": False, "error": "Document not found"}, status=404)

def custom_404_view(request, exception=None):
    """Custom 404 error page handler"""
    return render(request, '404page.html', status=404)

