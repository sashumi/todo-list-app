# Import the necessary modules
import unittest
from flask import url_for
from flask_testing import TestCase

# import the app's classes and objects
from application import app, db
from application.models import Tasks

# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # Create table
        db.create_all()

        # Create test registree
        task1 = Tasks(description="My First Task")

        # save users to database
        db.session.add(task1)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

# Write a test class for testing that the home page loads but we are not able to run a get request for delete and update routes.
class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code,200)

    def test_update_get(self):
        response = self.client.get(url_for('update', id=1))
        self.assertEqual(response.status_code,200)

    def test_delete_get(self):
        response = self.client.get(url_for('delete', id=1), follow_redirects=True)
        self.assertEqual(response.status_code,200)

class TestAdd(TestBase):
    def test_add_post(self):
        response = self.client.post(
            url_for('create'),
            data = dict(description="New task"),
            follow_redirects = True
        )
        self.assertIn(b'New task',response.data)

class TestUpdate(TestBase):
    def test_update_post(self):
        response = self.client.post(
            url_for('update', id=1),
            data = dict(description="Updated task"),
            follow_redirects=True
        )
        self.assertIn(b'Updated task',response.data)

class TestDelete(TestBase):
    def test_delete_post(self):
        response = self.client.get(
            url_for('delete', id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'New task',response.data)