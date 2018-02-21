# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['name']) < 2 or len(postData['username']) < 2:
            errors['name_error'] = 'Name and/or username must be 2 or more characters'
            
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not a valid email'
        
        if postData['birthday'] == '':
            errors['birthday'] = 'Please enter your birthday'
        
        if len(postData['password']) < 8 or len(postData['confirm_password']) <8:
            errors['pass_length'] = 'Password must be 8 or more characters'   

        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = 'Passwords do not match.'          

        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already in use."   
        return errors

    def login(self, postData):
        error ={}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) >0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = {"error":"Email/Password Invalid"}
                return errors
        else:
            errors = {"error":"Login Invalid"}
            return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    birthday = models.DateField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class ItemManager(models.Manager):
    def added_item(self, postData):
        errors = {}
        print postData
        if len(postData['item']) == 0:
            errors['item_error'] = "no empty entries"
        elif len(postData['item']) < 3:
            errors['item_error2'] ="The item must be at least 3 characters."
        elif len(postData['description']) == 0:
            errors['description'] ="Please enter a description."
        elif len(postData['image']) == 0:
            errors['image_error'] = "Please upload a valid url"
        elif len(postData['category']) == 0:
            errors['category_error'] = "Please select a category"
        if errors:
            print("Error adding everything")
            return errors
        else:
            print("Added everything successfully")
            user = User.objects.get(id = int(postData['added_by']))
            new_item = Item.objects.create(item = postData['item'], description = postData['description'], image = postData['image'], added_by = user )
            return {'new_item':new_item}

class Item(models.Model):
    item = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    category = models.CharField(max_length = 255, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    wished_by = models.ManyToManyField(User, related_name="wished_by")
    added_by = models.ForeignKey(User, related_name="item_added")
    objects = ItemManager()