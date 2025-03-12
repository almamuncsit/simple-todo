"""Test module for category routes."""
import json
from tests.base import BaseTestCase

class TestCategoryRoutes(BaseTestCase):
    """Test cases for category routes."""

    def test_get_categories_empty(self):
        """Test getting categories when none exist."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_category(self):
        """Test category creation."""
        data = {
            'name': 'Test Category',
            'description': 'Test Description'
        }
        response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test Category')
        self.assertEqual(response.json['description'], 'Test Description')

    def test_create_category_without_name(self):
        """Test category creation without name."""
        data = {'description': 'Test Description'}
        response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Name is required')

    def test_create_duplicate_category(self):
        """Test creating category with duplicate name."""
        data = {'name': 'Test Category'}
        self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Category name must be unique')

    def test_get_category(self):
        """Test getting a specific category."""
        # Create a category first
        data = {'name': 'Test Category'}
        create_response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        category_id = create_response.json['id']

        # Get the created category
        response = self.client.get(f'/api/categories/{category_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Category')

    def test_get_nonexistent_category(self):
        """Test getting a category that doesn't exist."""
        response = self.client.get('/api/categories/999')
        self.assertEqual(response.status_code, 404)

    def test_update_category(self):
        """Test updating a category."""
        # Create a category first
        data = {'name': 'Test Category'}
        create_response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        category_id = create_response.json['id']

        # Update the category
        update_data = {
            'name': 'Updated Category',
            'description': 'Updated Description'
        }
        response = self.client.put(
            f'/api/categories/{category_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Category')
        self.assertEqual(response.json['description'], 'Updated Description')

    def test_delete_category(self):
        """Test deleting a category."""
        # Create a category first
        data = {'name': 'Test Category'}
        create_response = self.client.post(
            '/api/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        category_id = create_response.json['id']

        # Delete the category
        response = self.client.delete(f'/api/categories/{category_id}')
        self.assertEqual(response.status_code, 204)

        # Verify category is deleted
        get_response = self.client.get(f'/api/categories/{category_id}')
        self.assertEqual(get_response.status_code, 404)
