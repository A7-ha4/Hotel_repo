from django.urls import path, include
from .views import auth_view, logout_view, register

urlpatterns = [
    path('home/', include('home.urls')),
    path('login/', auth_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register')
]