from django.urls import path

from users import views


urlpatterns = [
    path("signup/", views.CreateUserView.as_view(), name="SIGNUP"),
    path("login/", views.CreateTokenView.as_view(), name="LOGIN"),
    path("logout/", views.Logout.as_view(), name="LOGOUT"),
]