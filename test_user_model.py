"""User model tests."""

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




class UserModelTestCase(TestCase):
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

    

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_user_repr_method(self):
        """ Does the repr method work as expected """
        user = User(**user1)
        self.user = user
        res = f"<User #{self.user.id}: testuser1, test1@test.com>"
        self.assertEqual(user.__repr__(), res)

    def test_user_is_following_True(self):
        """ Does is_following successfully detect when user1 is following user2 """
        u1 = User(**user1)
        u2 = User(**user2)
        db.session.add_all([u1,u2])

        u1.following.append(u2)

        db.session.commit()

        self.assertTrue((u1.is_following(u2)))
        

    def test_user_is_following_False(self):
        """ Does is_following successfully detect when user1 is not following user2 """
        u1 = User(**user1)
        u2 = User(**user2)
        db.session.add_all([u1,u2])

        db.session.commit()

        self.assertFalse((u1.is_following(u2)))


    def test_user_is_followed_by_True(self):
        """ Does is_followed_by successfully detect when user1 is followed by user2"""
        u1 = User(**user1)
        u2 = User(**user2)
        db.session.add_all([u1,u2])

        u1.followers.append(u2)

        db.session.commit()

        self.assertTrue((u1.is_followed_by(u2)))


    def test_user_is_followed_by_True(self):
        """ Does is_followed_by successfully detect when user1 is not followed by user2"""
        u1 = User(**user1)
        u2 = User(**user2)
        db.session.add_all([u1,u2])

        db.session.commit()

        self.assertFalse((u1.is_followed_by(u2)))

    def test_valid_user_is_signed_up(self):
        """Does User.signup successfully create a new user given valid credentials"""
        u = user1
        User.signup(u['username'], u['email'], u['password'], User.image_url.default.arg)

        db.session.commit()
        user_in_db = User.query.filter_by(username='testuser1').first()
        self.assertEqual(user_in_db.username,u['username'])
        self.assertEqual(user_in_db.email,u['email'])

    def test_invalid_user_is_not_signed_up(self):
        """
        Does User.signup fail to create a new user if any of 
        the validations 
        (e.g. uniqueness, non-nullable fields) fail?
        """
        u1 = User(**user1)
        db.session.add(u1)
        db.session.commit()

        u2 = user2

        #Signup fails when username is already in db
        User.signup(
            username=user1['username'], 
            email=u2['email'], 
            password=u2['password'], 
            image_url=User.image_url.default.arg
        )

        with self.assertRaises(IntegrityError):
            db.session.commit()
        
        #signup fails when missing a non-nullable value
        with self.assertRaises(ValueError):
            User.signup(
                username=user2['username'],
                password=None, 
                email='email@email.com',
                image_url=User.image_url.default.arg
            )




        
        
