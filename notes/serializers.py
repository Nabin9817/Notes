from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Category
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id','name']
        
class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(many = True, queryset = Category.objects.all())
    
    class Meta:
        model = Note 
        fields = ['id','title','content','owner','category','created_at','updated_at']
        read_only_fields = ['owner','created_at','updated_at']
        

# ---------------------------
# Signup / Login Serializers
# ---------------------------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # inactive until email activation
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data