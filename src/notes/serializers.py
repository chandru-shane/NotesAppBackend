from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ["search_vector_field"]
        read_only_fields = ["owner",]
