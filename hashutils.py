#!/usr/bin/env python

__author__ = "Jeanna Clark"
__version__ = "1.0"
# July 2, 2017
# Flask Blog App Continued re: LaunchCode students
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


import bcrypt


def make_hash(string_password):
    return bcrypt.hashpw(bytes(string_password, 'utf-8'), bcrypt.gensalt(5))


def validate_password(input_string_password, stored_encrypted_password):
    return bcrypt.checkpw(input_string_password.encode('utf-8'), stored_encrypted_password.encode('utf-8'))
