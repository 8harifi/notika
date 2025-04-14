from django.urls import path

from core.views import (
    search_results_view,
    search_view,
    landin_view,
    favorites_view,
    upload_view,
    SignupView,
)
from django.contrib.auth.views import LoginView

app_name = 'core'

urlpatterns = [
    # login required
    path('search_results', view=search_results_view, name="search_results"),
    path('search', view=search_view, name="search"),
    path('favorites', view=favorites_view, name="favorites"),
    path('upload', view=upload_view, name="upload"),

    # login not required
    path('', view=landin_view, name="landing"),

    # auth
    path('login', view=LoginView.as_view(), name="login"),
    path('signup', view=SignupView.as_view(), name="signup"),
]

