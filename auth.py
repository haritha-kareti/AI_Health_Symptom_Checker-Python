"""
=========================================
AI Health Symptom Checker
Authentication Module
=========================================
"""

import sqlite3

from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

DATABASE = "database/users.db"


# ==========================================
# Database Connection
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# Create User Table
# ==========================================

def create_user_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)

    conn.commit()

    conn.close()


create_user_table()


# ==========================================
# Register User
# ==========================================

def register_user(fullname, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""

        INSERT INTO users
        (fullname,email,password)

        VALUES(?,?,?)

        """,

        (

            fullname,

            email,

            hashed_password

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==========================================
# Login User
# ==========================================

def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        if check_password_hash(

            user["password"],

            password

        ):

            return dict(user)

    return None


# ==========================================
# Get User
# ==========================================

def get_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


# ==========================================
# Delete User
# ==========================================

def delete_user(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM users WHERE email=?",

        (email,)

    )

    conn.commit()

    conn.close()


# ==========================================
# Login Required Decorator
# ==========================================

def login_required(function):

    @wraps(function)

    def wrapper(*args, **kwargs):

        if "user" not in session:

            flash(

                "Please login first.",

                "warning"

            )

            return redirect(

                url_for("login")

            )

        return function(

            *args,

            **kwargs

        )

    return wrapper


# ==========================================
# Logout
# ==========================================

def logout_user():

    session.clear()


# ==========================================
# Change Password
# ==========================================

def change_password(email, new_password):

    conn = get_connection()

    cursor = conn.cursor()

    password = generate_password_hash(new_password)

    cursor.execute(

        """

        UPDATE users

        SET password=?

        WHERE email=?

        """,

        (

            password,

            email

        )

    )

    conn.commit()

    conn.close()


# ==========================================
# Count Users
# ==========================================

def total_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    count = cursor.fetchone()[0]

    conn.close()

    return count