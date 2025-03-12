"""Test module for Flask application."""
from tests.base import BaseTestCase
from sqlalchemy import text

class TestApp(BaseTestCase):
    """Test cases for Flask application."""

    def test_app_creation(self):
        """Test Flask application creation."""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.testing)

    def test_db_connection(self):
        """Test database connection."""
        self.assertIn('sqlite', str(db.engine.url))
        result = db.session.execute(text('SELECT 1'))
        self.assertEqual(result.scalar(), 1)
