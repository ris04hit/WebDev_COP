from re import search
from bcrypt import hashpw
from cryptography.fernet import Fernet
from random import randint

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
    salt = b'$2b$12$BPgM2TZNwWMnrCl5d5Bjme'
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def gen_otp():
    otp=randint(100000,999999)
    return str(otp)