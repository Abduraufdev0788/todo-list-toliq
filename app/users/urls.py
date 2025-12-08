from django.urls import path
from .views import Register, Login, Logout, ProfileView, AdminPanelView, AdminUserManagment

urlpatterns = [
    path("auth/register/", Register.as_view()),
    path("auth/login/", Login.as_view()),
    path("auth/logout/", Logout.as_view()),

    #user
    path("auth/users/me/", ProfileView.as_view() ),
    path("auth/users/", AdminPanelView.as_view() ),
    path("auth/users/<int:pk>/", AdminUserManagment.as_view() ),


]
