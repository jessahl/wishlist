# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q


def index(request):
    return render(request, 'wish/index.html')

def about(request):
    return render(request, 'wish/about.html')

def contact(request):
    return render(request, 'wish/contact.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], email = request.POST['email'], birthday = request.POST['birthday'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")        
    return redirect('/dashboard')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/dashboard')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def users(request, user_id):
    context={"user": User.objects.get(id=user_id)}
    return render(request, 'wish/dashboard.html', context)

def wish_list(request):
    user = User.objects.get(id =request.session['id'])
    context={
        'user':user,
        'wished': Item.objects.filter(wished_by = user),
        'wished_by_others': Item.objects.exclude(wished_by = user),
        'added_by_others': Item.objects.exclude(added_by = user),
        'added_by': User.objects.get(id =request.session['id'])
    }
    return render(request, 'wish/dashboard.html', context)

def wishlists(request):
    user = User.objects.get(id =request.session['id'])
    context={
        'user':user,
        'wished': Item.objects.filter(wished_by = user)
    }
    return render(request, 'wish/wishlists.html', context)

def test_wish_list(request):
    user = User.objects.get(id =request.session['id'])
    context={
        'user':user,
        'wished': Item.objects.filter(wished_by = user),
        'wished_by_others': Item.objects.exclude(wished_by = user),
        'added_by_others': Item.objects.exclude(added_by = user),
        'added_by': User.objects.get(id =request.session['id'])
    }
    return render(request, 'wish/test_dashboard.html', context)

def other_items(request):
    user = User.objects.get(id =request.session['id'])
    context={
        'user':user,
        'wished': Item.objects.filter(wished_by = user),
        'wished_by_others': Item.objects.exclude(wished_by = user),
        'added_by_others': Item.objects.exclude(added_by = user),
        'added_by': User.objects.get(id =request.session['id'])
    }
    return render(request, 'wish/other_items.html', context)

def items(request, item_id):
    context = {
    'item': Item.objects.get(id = item_id)  
    }
    return render(request, 'wish/wish_items.html', context)

def create(request):
    return render (request, 'wish/create.html')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
        messages.success(request, "You have logged out")
    return redirect('/')

def added_item(request):
    print
    error_2 = Item.objects.added_item(request.POST)
    if 'errors' in error_2:
        for error in error_2:
            print error_2[error]
            messages.error(request, error_2[error])
        return redirect('wish/create')
    else:
        user = User.objects.get(id =request.session['id'])
        item1 = Item.objects.create(item = request.POST['item'], description = request.POST['description'], image = request.POST['image'], added_by = user)
        item1.wished_by.add(user)
        item1.save()
        messages.error(request, "You have successfully added an item")        
        return redirect('/dashboard')

def add_wish(request, item_id):
    item = Item.objects.get(id = item_id)
    user = User.objects.get(id =request.session['id'])
    item.wished_by.add(user)
    return redirect('/dashboard')

def unwish(request, item_id):
    item = Item.objects.get(id = item_id)
    user = User.objects.get(id =request.session['id'])
    item.wished_by.remove(user)
    return redirect('/dashboard')

def delete(request, item_id):
    item = Item.objects.get(id = item_id)
    context = {
        'item': item
    }
    return render(request, 'wish/delete.html', context)

def destroy(request, item_id):
    Item.objects.get(id = item_id).delete()
    return redirect('/dashboard')

def update(request, item_id):
    item = Item.objects.get(id = item_id)
    context = {
        'item': item
    }
    return render(request, 'wish/update.html', context)

def edit(request, item_id):
    item = Item.objects.get(id = item_id)
    item.item = request.POST['item']
    item.save()
    messages.error(request, "You have successfully updated an item")
    return redirect('/dashboard')