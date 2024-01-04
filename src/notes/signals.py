from django.contrib.postgres.search import SearchVector
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Note


@receiver(post_save, sender=Note, dispatch_uid="update_search_vector")
def update_stock(sender, instance, created, **kwargs):
    Note.objects.filter(id=instance.id).update(search_vector_field=SearchVector("title", "content"))