"""Test module for frontend routes."""
from http import HTTPStatus
from tests.base import BaseTestCase


class TestFrontendRoutes(BaseTestCase):
    """Test cases for frontend routes."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.app.config.update({
            'SERVER_NAME': 'localhost:5000',
            'PREFERRED_URL_SCHEME': 'http',
            'TESTING': True
        })

    def test_home_page_success(self):
        """Test successful home page access."""
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn(b'Todo App', response.data)
            self.assertIn(b'Welcome', response.data)
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_home_page_method_not_allowed(self):
        """Test home page with invalid HTTP method."""
        with self.app.test_client() as client:
            response = client.post('/')
            self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_categories_page_success(self):
        """Test successful categories page access."""
        with self.app.test_client() as client:
            response = client.get('/categories')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn(b'Categories', response.data)
            self.assertIn(b'Add Category', response.data)
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_categories_page_method_not_allowed(self):
        """Test categories page with invalid HTTP method."""
        with self.app.test_client() as client:
            response = client.post('/categories')
            self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_categories_page_template(self):
        """Test if categories page uses correct template."""
        with self.app.test_client() as client:
            response = client.get('/categories')
            self.assert_template_used('categories.html')
            self.assertIn(b'categoryModal', response.data)

    def test_tasks_page_success(self):
        """Test successful tasks page access."""
        with self.app.test_client() as client:
            response = client.get('/tasks')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn(b'Tasks', response.data)
            self.assertIn(b'Add Task', response.data)
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_tasks_page_method_not_allowed(self):
        """Test tasks page with invalid HTTP method."""
        with self.app.test_client() as client:
            response = client.post('/tasks')
            self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_tasks_page_template(self):
        """Test if tasks page uses correct template."""
        with self.app.test_client() as client:
            response = client.get('/tasks')
            self.assert_template_used('tasks.html')
            self.assertIn(b'taskModal', response.data)

    def test_invalid_route(self):
        """Test accessing invalid route."""
        with self.app.test_client() as client:
            response = client.get('/invalid-route')
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def assert_template_used(self, template_name):
        """Helper method to assert template usage.

        Args:
            template_name (str): Name of the template to check

        Raises:
            AssertionError: If template is not found
        """
        templates = self.app.jinja_env.list_templates()
        self.assertTrue(
            template_name in templates,
            f"Template {template_name} not found in available templates: {templates}"
        )