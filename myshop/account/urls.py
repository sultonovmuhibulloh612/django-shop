from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [ 
    path('', include('django.contrib.auth.urls')),
    path('', views.user_detail, name='user_detail'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),  
]