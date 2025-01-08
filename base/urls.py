from django.urls import path
from . import views

urlpatterns = [
    path('login/' , views.loginpage ,name = "login"),
    path('logout/' , views.logoutpage ,name = "logout"),
    path('register/' , views.registerpage ,name = "register"),
    path("", views.home , name="home"),
    path("room/<int:pk>/" , views.room , name = "room"),
    path('create-room/', views.createRoom , name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom , name = "update-room"),
    path('delete-room/<str:pk>/', views.delete_room , name = "delete-room"),
    path('profile/' , views.profilepage ,name = "profile"),
]
