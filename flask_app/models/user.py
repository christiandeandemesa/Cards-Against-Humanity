from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name'] # Anything here and below will change to reflect what columns the table in your database has.
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        result = connectToMySQL('television').query_db(query, data)
        return result

    @classmethod
    def read_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('television').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def read_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL('television').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def read_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('television').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def valid_register(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL('television').query_db(query, user)
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.', 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.', 'register')
            is_valid = False
        if len(result) >= 1:
            flash('Email is already taken.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email.', 'register')
            is_valid = False
        if len(user['password']) < 10:
            flash('Password must be at least 10 characters.', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords do not match.', 'register')
        return is_valid