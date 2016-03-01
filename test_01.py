import os
import unittest

from app import app
from db import db
from models import User

basedir = ""


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        print " * created"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users(self):
    	# create user
        u = User(name='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()

        # read users
        all_users = db.session.query(User).all()
    	self.assertEqual(len(all_users), 1)

    	# read by name
        user_john = db.session.query(User).filter_by(name="john").one()
    	self.assertEqual(user_john.email, "john@example.com")


if __name__ == '__main__':
    unittest.main()
