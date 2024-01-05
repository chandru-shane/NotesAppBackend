import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import Note
from users.models import User


import pytest



@pytest.mark.django_db
def test_note_list_create_api_view_unauthenticated_user():

    client = APIClient()
    response = client.post(reverse("NOTE_LIST_CREATE_API_VIEW"), {"title": "Test Note", "content": "Test Content"})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Note.objects.all().count() == 0


@pytest.mark.django_db
def test_note_list_create_api_view_authenticated_user():
    user = User.objects.create(username="testuser", email="testuser@example.com", password="testpassword")

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(reverse("NOTE_LIST_CREATE_API_VIEW"), {"title": "Test Note", "content": "Test Content"})
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Note.objects.filter(owner=user).count() == 1
    
    response = client.get(reverse("NOTE_LIST_CREATE_API_VIEW"))
    assert len(response.data) == 1



@pytest.mark.django_db
def test_note_rud_api_view_authenticated_user_update():
    user1 = User.objects.create(username="testuser01", email="testuser01@example.com", password="testpassword")

    # Log in the user and create a note
    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.post(reverse("NOTE_LIST_CREATE_API_VIEW",), {"title": "Test Note", "content": "Test Content"})
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Note.objects.filter(owner=user1).count() == 1

    response = client.patch(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new title"})
    assert response.status_code == status.HTTP_200_OK
    assert Note.objects.filter(owner=user1).first().title == "new title"
    
    user2 = User.objects.create(username="testuser02", email="testuser02@example.com", password="testpassword")
    
    client.force_authenticate(user=user2)
    
    response = client.patch(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Note.objects.filter(owner=user1).first().title != "new"

    response = client.get(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.delete(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Note.objects.filter(owner=user1).count() == 1

    client.force_authenticate(user=user1)
    response = client.get(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new"})
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(reverse("NOTE_RUD_API_VIEW",kwargs={"pk": Note.objects.filter(owner=user1).first().id}), {"title": "new"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Note.objects.filter(owner=user1).count() == 0


    

@pytest.mark.django_db
def test_note_search_api_view_authenticated_user():
    user = User.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
    client = APIClient()
    client.force_authenticate(user=user)

    # Create a note for the user
    note = Note.objects.create(title="Test Note", content="Test Content", owner=user)
   

    response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Test"})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.json()[0]["id"] == note.id

    note = Note.objects.create(title="New Note", content="Test Content", owner=user)
    response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Note"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Physics"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


    user2 = User.objects.create(username="testuser02", email="testuser02@example.com", password="testpassword")
    client.force_authenticate(user=user2)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
    



@pytest.mark.django_db
def test_note_search_api_view_unauthenticated_user():
    client = APIClient()
    # Create a note for the user
   

    response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Test"})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_throttle():
    user = User.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
    client = APIClient()
    client.force_authenticate(user=user)

    # Create a note for the user
    note = Note.objects.create(title="Test Note", content="Test Content", owner=user)
   

    for _ in range(1000):
        response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Test"})
        assert response.status_code == status.HTTP_200_OK
    
    response = client.get(reverse("SEARCH_API_VIEW"), {"q": "Test"})
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    