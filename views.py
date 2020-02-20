import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create views here!
def index(request):
    return render(request, "index.html")

def create_user(request):
    errors = User.objects.new_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")

    else:
        newFirstName = request.POST["first_name"]
        newLastName = request.POST["last_name"]
        newEmail = request.POST["email"]
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print("pw_hash")
        new_user = User.objects.create(first_name=newFirstName, last_name=newLastName, email=newEmail, password=pw_hash)
        request.session["user_id"] = new_user.id
        print("User Submitted!!!!!!")
        return redirect("/success")

def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "new_user" : User.objects.get(id=request.session["user_id"])
    }
    return render(request, "success.html", context)

def proc_login(request):
    if request.method != "POST":
        return redirect("/")
    valid = User.objects.login_validator(request.POST)
    if len (valid["errors"]) > 0:
        for key, value in valid["errors"].items():
            messages.error(request,value)
        return redirect("/")
    else:
        request.session["user_id"] = valid["user"].id
        return redirect ("/success")
    
    

def logout(request):
    request.session.clear()
    return redirect ("/")

