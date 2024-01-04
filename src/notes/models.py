from django.db import models
from django.contrib.postgres.search import SearchVectorField      
from django.contrib.postgres.indexes import GinIndex

from users.models import User
# Create your models here.




class Note(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=2**16)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes_owner")
    search_vector_field = SearchVectorField()
    class Meta:
        indexes = [GinIndex(fields=['search_vector_field'])]