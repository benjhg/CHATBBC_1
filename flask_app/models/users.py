from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template, request, redirect, flash, session
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "global_chat"
    def __init__(self, data):
        self.id = data.get('id')
        self.username = data.get('username')
        self.email = data.get('email')
        self.password = data.get('password')
        self.alias = data.get('alias')
        self.updated_at = data.get('updated_at')
        self.created_at = data.get('created_at')
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password, alias, created_at) VALUES (%(username)s, %(email)s, %(password)s, %(alias)s, NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def obtener_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        user_data = connectToMySQL(cls.db_name).query_db(query, data)
        if user_data:
            # Si se encontró un usuario con ese ID, crea y devuelve un objeto User
            user = cls(user_data[0])
            return user
        else:
            # Si no se encontró un usuario con ese ID, devuelve None
            return None

    @staticmethod
    def validate_register(user):
        is_valid = True

        # Validaciones del formulario
        if len(user['username']) < 3:
            flash("El nombre de usuario debe tener al menos 3 caracteres.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Correo electrónico inválido.", "register")
            is_valid = False
        if len(user['password']) < 6:  # Ajusta la longitud mínima de la contraseña según tus requisitos
            flash("La contraseña debe tener al menos 6 caracteres.", "register")
            is_valid = False
        if user['password'] != request.form['confirm']:
            flash("Las contraseñas no coinciden.", "register")
            is_valid = False

        # Verificar si el correo electrónico ya está en uso
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)
        if len(results) > 0:
            flash("El correo electrónico ya está en uso.", "register")
            is_valid = False

        return is_valid     