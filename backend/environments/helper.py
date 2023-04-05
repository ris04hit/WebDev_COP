from re import search
from bcrypt import hashpw, gensalt, checkpw

def password_strength(password):
    length = len(password)
    if length < 8:
        return -1
    elif length < 12:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password):
            return 0
    else:
        if search('[a-z]', password) and search('[A-Z]', password) \
        and search('[0-9]', password) and search('[^a-zA-Z0-9]', password):
            return 1
    return 0

def hash_pwd(password):
    password = "MyP@ssw0rd!"
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

def check_pwd(password, hashed_password):
    checkpw(password.encode('utf-8'), hashed_password)