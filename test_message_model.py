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

    def test_msg_repr_method(self):
        """ Does the repr method work as expected """
        user = User(**user1)
        db.session.add(user)

        msg = Message(
            text="TEST MESSAGE",
            user_id=user.id)
        user.messages.append(msg)
        db.session.commit()
        res = f"<Message_id: {msg.id}: TEST MESSAGE, user_id: {msg.user_id}>"
        self.assertEqual(msg.__repr__(), res)
    
    def test_user_messages_includes_msg(self):
        """ Does user.messages include the new message """

        user = User(**user1)
        db.session.add(user)

        msg = Message(
            text="TEST MESSAGE",
            user_id=user.id)
        user.messages.append(msg)
        db.session.commit()

        self.assertEqual(len(user.messages), 1)
        self.assertIn(msg, user.messages)
    
    def test_user_liked_messages_includes_msg(self):
        """ Does user.messages include the new message """

        u1 = User(**user1)
        u2 = User(**user2)

        db.session.add_all([u1,u2])

        msg = Message(
            text="TEST MESSAGE",
            user_id=u2.id)
        u2.messages.append(msg)
        u1.liked_messages.append(msg)
        db.session.commit()

        self.assertEqual(len(u1.liked_messages), 1)
        self.assertIn(msg, u1.liked_messages)