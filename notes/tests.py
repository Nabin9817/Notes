from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from notes.models import Note, Category

class NotelyBackendTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password, 
            email='test@notely.com'
        )
        
        # Create a category
        self.category = Category.objects.create(name="Study", owner=self.user)
        
        # Create a sample note
        self.note = Note.objects.create(
            title="Initial Note",
            content="Initial Content",
            owner=self.user
        )
        self.note.category.add(self.category)

    # --- AUTHENTICATION TESTS ---
    def test_registration(self):
        url = reverse('register')
        data = {"username": "newuser", "email": "new@notely.com", "password": "pass123password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_jwt_flow(self):
        url = reverse('login')
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # --- NOTE TESTS (PAGINATION AWARE) ---
    def test_list_notes(self):
        """Fixed: Accessing 'results' because of PageNumberPagination."""
        self.client.force_authenticate(user=self.user)
        url = reverse('note-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if 'results' exists (Pagination is active)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['count'], 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_create_note_with_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('note-list-create')
        data = {
            "title": "New Note",
            "content": "Testing content",
            "category": [self.category.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_note_detail(self):
        """Detail views are NOT paginated, so response.data is the object itself."""
        self.client.force_authenticate(user=self.user)
        url = reverse('note-detail', kwargs={'pk': self.note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.note.title)

    # --- CATEGORY TESTS (PAGINATION AWARE) ---
    def test_list_categories(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Categories also use pagination in your CategoryListCreateView
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_delete_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)