from django.urls import path
from django.http import Http404

from core.views import (
    search_results_view,
    search_view,
    landin_view,
    favorites_view,
    upload_view,
    SignupView,
    edit_profile_view,
    download_document,
    add_favorite,
    toggle_favorite,
    document_info,
    custom_404_view,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'core'

def test_404_view(request):
    """Test view to trigger 404 page"""
    raise Http404("This is a test 404 page")

urlpatterns = [
    # login required
    path('search-results', view=search_results_view, name="search_results"),
    path('search', view=search_view, name="search"),
    path('favorites', view=favorites_view, name="favorites"),
    path('upload', view=upload_view, name="upload"),
    path('edit-profile', view=edit_profile_view, name="edit_profile"),
    path('download/<int:doc_id>/', view=download_document, name='download'),
    path('favorite/add', view=add_favorite, name='add_favorite'),
    path('favorite/toggle', view=toggle_favorite, name='toggle_favorite'),
    path('document/<int:doc_id>/info', view=document_info, name='document_info'),

    # login not required
    path('', view=landin_view, name="landing"),

    # auth
    path('login', view=LoginView.as_view(), name="login"),
    path('logout', view=LogoutView.as_view(next_page='/'), name="logout"),
    path('signup', view=SignupView.as_view(), name="signup"),
    
    # test 404 page
    path('test-404', view=test_404_view, name="test_404"),
    path('404-preview', view=custom_404_view, name="404_preview"),
]

