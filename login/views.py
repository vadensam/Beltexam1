from django.shortcuts import render, redirect, HttpResponse
from .models import User, Wish, Granted
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        fname = request.POST['fname'],
        lname = request.POST['lname'],
        email = request.POST['email'],
        password = pw_hash,
    )
    request.session['id'] = user.id
    return redirect(home)

def login(request):
    user_db = User.objects.filter(email=request.POST['email'])
    if user_db:
        log_user = user_db[0]

        if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
            request.session['id'] = log_user.id
            return redirect(home)

    messages.error(request, 'Incorrect email or password.')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    user = User.objects.get(id=request.session['id'])
    wishes = user.wishes.all()
    granted = Granted.objects.all()
    to_exclude = [wish.grant.id for wish in granted]
    ungranted = Wish.objects.filter(user = user).exclude(id__in=to_exclude)
    context = {
        'user':user,
        'ungranted': ungranted,
        'granted' : Granted.objects.all()
    }
    return render(request, 'home.html', context)

def make_wish(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
        
    }
    return render(request, 'wishmake.html', context)

def process_wish(request):
    user = User.objects.get(id=request.session['id'])
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(make_wish)

    wish = Wish.objects.create(
        item = request.POST['item'],
        desc = request.POST['desc'],
        user = user
    )
    return redirect(home)

def grant(request, id):
    wish = Wish.objects.get(id=id)
    Granted.objects.create(
        grant = wish
    )
    return redirect(home)

def edit(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    context = {
        'wish': wish,
        'user': user
    }
    return render(request, 'edit.html', context)

def edit_wish(request):
    wish = Wish.objects.get(id=request.POST['wish_id'])
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(edit, wish.id)

    wish.item = request.POST['item']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect(home)

def remover(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect(home)

def like_me(request, id):
    user = User.objects.get(id = request.session['id'])
    like = Granted.objects.get(id=id)
    like.liker.add(user)
    num = len(like.liker.all())
    like.number = num
    like.save()
    return redirect(home)

def stats(request):
    user = User.objects.get(id=request.session['id'])
    wishes = user.wishes.all()
    granted = Granted.objects.all()
    to_exclude = [wish.grant.id for wish in granted]
    ungranted = Wish.objects.filter(user = user).exclude(id__in=to_exclude)
    my_granted = Wish.objects.filter(user = user).filter(id__in=to_exclude)
    
    context = {
        'user':user,
        'ungranted': len(ungranted),
        'granted' : len(Granted.objects.all()),
        'my_gran' : len(my_granted)
    }
    return render(request, 'stats.html', context)