from django.urls import path

from core.views import (
    search_results_view,
)

app_name = 'core'

urlpatterns = [
    path('search_results', view=search_results_view, name="search_results"),
]

