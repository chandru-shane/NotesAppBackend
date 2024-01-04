from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerPermission

# Create your views here.
"""
Implement list all notes
Create notes
RUD notes
Post share notes
GET /api/search?q=:query: search for notes based on keywords for the authenticated user.
"""

class NoteListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class NoteRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class NoteShareAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class NoteSearchAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("q")
        result = Note.objects.filter(owner=self.request.user, search_vector_field=search_query)
        return Response(self.get_serializer(result, many=True).data, status=status.HTTP_200_OK)