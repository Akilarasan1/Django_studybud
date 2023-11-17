from django.urls import path
from .import views

urlpatterns =[
        path('login/', views.loginPage,name='login'),
        path('logout/',  views.logoutUser,name='logout'),
        path('register/', views.registerUser, name= 'register'),
        
        path('', views.home,name='home'),
        path('profile/<str:pk>/', views.userProfile, name="profile"),
        path('room/<str:pk>/', views.room, name="room"),
        
        path('create-room/', views.createRoom, name = 'create-room'),
        path('update-room/<str:pk>/', views.updateRoom, name = 'update-room'),
        path('delete-room/<str:room_id>/', views.deleteRoom, name='delete-room'),
        path('delete-message/<str:room_id>/', views.deleteMessage, name='delete-message'),
        path('update-user/', views.updateUser, name='update-user'),
        path('topics/', views.topicsPage, name='topics'),
         path('activity/', views.activityPage, name='activity')
    ]
