from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:
    db = "fields_wedding_db"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.plus_one = data['plus_1']
        self.food_option = data['food']
        self.plus_one_food = data['plus_one_food']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,email,plus_1,food,plus_one_food,created_at) VALUES(%(name)s,%(email)s,%(plus_1)s,%(food)s,%(plus_one_food)s,NOW())"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        print(users)
        return users

    @classmethod
    def get_all_plus_ones(cls):
        query = "SELECT * FROM users WHERE plus_1 != 0;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        print(users)
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,user_id)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","rsvp")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","rsvp")
            is_valid=False
        if len(user['name']) < 2:
            flash("Name must be at least 2 characters","rsvp")
            is_valid= False
        if len(user['food']) < 1:
            flash("Select a food option","rsvp")
            is_valid= False
        if not user['plus_1'] != '1' and user['plus_1'] != '0':
            flash("Select a valid guest option","rsvp")
            is_valid= False
        if user['plus_1'] == 1 and len(user['plus_one_food']) < 1:
            flash("Select a food option for your guest","rsvp")
            is_valid= False
        if user['invite_code'] != 'fields24':
            flash("Please enter your invite code","rsvp")
            is_valid= False
        return is_valid

    @staticmethod
    def validate_admin(user):
        is_valid= True

        if user['user'] != 'admin':
            is_valid = False
        if user['pass'] != 'admin':
            is_valid = False

        return is_valid