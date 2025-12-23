"""
URL configuration for note_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from notes.views import (
    LogoutAPIView,SignupAPIView, LoginAPIView,
    NoteListCreateView, NoteDetailView,CategoryListCreateView, CategoryDetailView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # REST API endpoints
    # --- AUTHENTICATION ---
    # User Registration & Login
    path('api/register/', SignupAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    # JWT Token Refresh (used to get a new access token when old one expires)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- NOTES ---
    # List all notes (Search/Sort) and Create a new note
    path('api/notes/', NoteListCreateView.as_view(), name='note-list-create'),
    # Retrieve, Update, or Delete a specific note by ID
    path('api/notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),

    # --- CATEGORIES ---
    # List all categories and Create a new one
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    # Retrieve, Update, or Delete a specific category by ID
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),  
]
