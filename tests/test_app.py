import unittest
import os
from app import create_app, db

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_app_creation(self):
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.testing)

    def test_db_connection(self):
        # Check if the database URL is using SQLite memory database
        self.assertIn('sqlite', str(db.engine.url))
        result = db.session.execute('SELECT 1')
        self.assertEqual(result.scalar(), 1)

if __name__ == '__main__':
    unittest.main()