"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, bcrypt, User, Message, Follows
from sqlalchemy.exc import IntegrityError


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

user1 = {
            'email':"test1@test.com",
            'username':"testuser1",
            'password':"HASHED_PASSWORD"
        }

user2 = {
            'email':"test2@test.com",
            'username':"testuser2",
            'password':"HASHED_PASSWORD"
        }



class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback() 

    