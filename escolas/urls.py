
from django.urls import path

from .views import SchoolListView


urlpatterns = [
    path("escolas/", SchoolListView.as_view(), name="escola-list"),
]
