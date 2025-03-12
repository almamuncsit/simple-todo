"""Models initialization module."""
from app.models.category import Category
from app.models.task import Task

# Initialize relationships after both models are defined
Category.tasks = Category.tasks