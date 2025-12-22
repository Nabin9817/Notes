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
    LogoutAPIView, NoteList, NoteDetail, CategoryList, CategoryDetail,
    SignupAPIView, LoginAPIView, NoteListCreateView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # REST API endpoints
    path('api/auth/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/createnote/', NoteListCreateView.as_view(),name ='create-note'),
    #path('api/notes/', NoteList.as_view(), name='api-note-list'),
    path('api/notes/<int:pk>/', NoteDetail.as_view(), name='api-note-detail'),
    path('api/categories/', CategoryList.as_view(), name='api-cat-list'),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='api-catdetail'),
    #path('api/auth/activate/<uidb64>/<token>/', ActivateAccountAPIView.as_view(), name='activate'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    
    
    
]
