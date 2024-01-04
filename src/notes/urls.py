from django.urls import path
from .views import (
    NoteListCreateAPIView,
    NoteRUDAPIView,
    NoteShareAPIView
)

urlpatterns = [
    path("", NoteListCreateAPIView.as_view(), name="NOTE_LIST_CREATE_API_VIEW"),
    path("<int:pk>/", NoteRUDAPIView.as_view(), name="NOTE_RUD_API_VIEW"),
    path("<int:pk>/share/", NoteShareAPIView.as_view(), name="SHARE_API_VIEW"),
]
