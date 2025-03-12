"""Test module for task routes."""
import json
from datetime import datetime, timedelta
from tests.base import BaseTestCase
from app.models.category import Category
from app.extensions import db

class TestTaskRoutes(BaseTestCase):
    """Test cases for task routes."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        # Create a test category
        self.category = Category(name='Test Category')
        db.session.add(self.category)
        db.session.commit()

    def test_get_tasks_empty(self):
        """Test getting tasks when none exist."""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_task(self):
        """Test task creation with all fields."""
        due_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'status': 'pending',
            'category_id': self.category.id,
            'due_date': due_date
        }
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'Test Task')
        self.assertEqual(response.json['priority'], 'high')
        self.assertEqual(response.json['category_id'], self.category.id)

    def test_create_task_without_title(self):
        """Test task creation without required title."""
        data = {'description': 'Test Description'}
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Title is required')

    def test_create_task_invalid_date(self):
        """Test task creation with invalid date format."""
        data = {
            'title': 'Test Task',
            'due_date': 'invalid-date'
        }
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid date format')

    def test_create_task_invalid_category(self):
        """Test task creation with invalid category ID."""
        data = {
            'title': 'Test Task',
            'category_id': 999
        }
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid category ID')

    def test_get_task(self):
        """Test getting a specific task."""
        # Create a task first
        data = {'title': 'Test Task'}
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        task_id = create_response.json['id']

        # Get the created task
        response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Test Task')

    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        response = self.client.get('/api/tasks/999')
        self.assertEqual(response.status_code, 404)

    def test_update_task(self):
        """Test updating a task."""
        # Create a task first
        data = {'title': 'Test Task'}
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        task_id = create_response.json['id']

        # Update the task
        update_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 'low',
            'status': 'completed'
        }
        response = self.client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Updated Task')
        self.assertEqual(response.json['priority'], 'low')
        self.assertEqual(response.json['status'], 'completed')

    def test_delete_task(self):
        """Test deleting a task."""
        # Create a task first
        data = {'title': 'Test Task'}
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        task_id = create_response.json['id']

        # Delete the task
        response = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 204)

        # Verify task is deleted
        get_response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(get_response.status_code, 404)
