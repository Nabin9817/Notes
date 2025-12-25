from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Category
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id', 'name']

class NoteSerializer(serializers.ModelSerializer):
    """ Used for GET requests: Displays full data including category names """
    owner = serializers.ReadOnlyField(source='owner.username')
    category_names = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='name', 
        source='category'
    )
    
    class Meta:
        model = Note 
        fields = [
            'id', 'title', 'content', 'owner', 
            'category', 'category_names', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

class NoteCreateSerializer(serializers.ModelSerializer):
    """ Used for POST/PUT requests: Handles IDs for category assignment """
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Note
        fields = ["id", "title", "content", "category", "created_at"]

    def create(self, validated_data):
        categories = validated_data.pop("category", [])
        note = Note.objects.create(**validated_data)
        note.category.set(categories)
        return note

    def update(self, instance, validated_data):
        categories = validated_data.pop("category", None)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        if categories is not None:
            instance.category.set(categories)
        return instance

# --- AUTH SERIALIZERS ---

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data