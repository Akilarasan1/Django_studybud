from django.urls import path
from . import views

urlpatterns =[ path('login/', views.loginPage,name='login'),path('', views.home,name='home'),
              
              path('logout/',  views.logoutUser,name='logout'),
              path('register/', views.registerUser, name= 'register'),
    # path('room/', views.room, name = 'room'),
        path('room/<str:pk>/', views.room, name="room"),
        path('create-room/', views.createRoom, name = 'create-room'),
        path('update-room/<str:pk>/', views.updateRoom, name = 'update-room'),
      #  path('delete-room/<str:pk>/', views.deleteRoom, name = 'delete-room'),
        path('delete-room/<int:room_id>/', views.deleteRoom, name='delete-room'),
    ]
