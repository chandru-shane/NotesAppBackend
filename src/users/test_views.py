import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User


@pytest.mark.django_db
def test_register_view():
    client = APIClient()
    # invalid email is used request should return 400
    response = client.post(
        reverse("SIGNUP"), {"email": "testuser1@.com", "username": "testuser1", "password": "testuser1"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0

    response = client.post(
        reverse("SIGNUP"), {"email": "testuser1@example.com", "username": "testuser1", "password": "testuser1"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_login_view():
    client = APIClient()
    # invalid email is used request should return 400
    user = User.objects.create(**{"email": "testuser1@example.com", "username": "testuser1"})
    user.set_password("testuser1")
    user.save()

    response = client.post(reverse("LOGIN"), {"username_or_email": "testuser1@example.com", "password": "testuser1"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("token", False)
    # with worng creds
    response = client.post(reverse("LOGIN"), {"username_or_email": "testuser1@example.com", "password": "estuser1"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get("token", False)
