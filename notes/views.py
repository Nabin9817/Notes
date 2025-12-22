from urllib import request
from rest_framework import generics, permissions, filters,status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Note, Category
from .serializers import NoteCreateSerializer, NoteSerializer, CategorySerializer, SignupSerializer, LoginSerializer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.urls import reverse

class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__id']
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        # Return notes for this user only
        user = self.request.user
        queryset = Note.objects.filter(owner=user)
        # Optionally filter by query param 'category'
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset.order_by('-updated_at')

    def perform_create(self, serializer):
        # Assign the note's owner to the logged-in user
        serializer.save(owner=self.request.user)
        
        
class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(owner=request.user).order_by("-created_at")
        serializer = NoteCreateSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Ensures users can only access their own note
        return Note.objects.filter(owner=self.request.user)
    
class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch ALL categories from the database so the user can pick any
        categories = Category.objects.all() 
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name', '').strip()
        # Logic: If it exists, return it. If not, create it.
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'owner': request.user}
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    


# ---------------------------
# Signup API
# ---------------------------
class SignupAPIView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Make user active immediately
            user.is_active = True
            user.save()

            return Response(
                {"message": "Account created successfully. You can log in now."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Login API
# ---------------------------
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        # No need to check user.is_active
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=200)

        
        
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)
    
    
'''
class ActivateAccountAPIView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully"})
        return Response({"error": "Invalid activation link"}, status=400)
    '''
