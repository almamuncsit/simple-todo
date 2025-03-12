"""Test module for frontend routes."""
from http import HTTPStatus
from tests.base import BaseTestCase


class TestFrontendRoutes(BaseTestCase):
    """Test cases for frontend routes."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up test environment."""
        super().tearDown()
        self.app_context.pop()

    def test_home_page_success(self):
        """Test successful home page access."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b'Todo App', response.data)
        self.assertIn(b'Welcome', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_home_page_method_not_allowed(self):
        """Test home page with invalid HTTP method."""
        response = self.client.post('/')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_categories_page_success(self):
        """Test successful categories page access."""
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b'Categories', response.data)
        self.assertIn(b'Add Category', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_categories_page_method_not_allowed(self):
        """Test categories page with invalid HTTP method."""
        response = self.client.post('/categories')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_categories_page_template(self):
        """Test if categories page uses correct template."""
        with self.client:
            response = self.client.get('/categories')
            self.assert_template_used('categories.html')
            self.assertIn(b'categoryModal', response.data)

    def test_tasks_page_success(self):
        """Test successful tasks page access."""
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b'Tasks', response.data)
        self.assertIn(b'Add Task', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_tasks_page_method_not_allowed(self):
        """Test tasks page with invalid HTTP method."""
        response = self.client.post('/tasks')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_tasks_page_template(self):
        """Test if tasks page uses correct template."""
        with self.client:
            response = self.client.get('/tasks')
            self.assert_template_used('tasks.html')
            self.assertIn(b'taskModal', response.data)

    def test_invalid_route(self):
        """Test accessing invalid route."""
        response = self.client.get('/invalid-route')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def assert_template_used(self, template_name):
        """Helper method to assert template usage.

        Args:
            template_name (str): Name of the template to check

        Raises:
            AssertionError: If template is not found
        """
        self.assertTrue(
            template_name in [t.name for t in self._ctx.app.jinja_env.list_templates()],
            f"Template {template_name} not found"
        )