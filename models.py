from __future__ import unicode_literals
import re, bcrypt
from django.db import models


# Create your models here.
class UserManager(models.Manager):
    def new_validator(self, postData):
        errors = {}    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be 8 characters or more"
        if (postData["password"] != postData["confirmed_password"]):
            errors ["password"] = "Passwords do not match"
        return errors

    def login_validator(self,postData):
        valid = {
            "errors" : {},
        }
        user = self.filter(email=postData["login_email"])
        if user:
            existing_user=user[0]
            if not bcrypt.checkpw(postData["login_password"].encode(),existing_user.password.encode()):
                valid["errors"]["login_password"] = "Password is incorrect"
            else:
                valid["user"] = existing_user
        else:
            valid["errors"]["login_email"] = "Email not found"
        return valid
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

