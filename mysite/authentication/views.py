from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserAccount

def login(request):
    context = {"account_type": None}  # Ensure 'account_type' is always in context

    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password")
        account_type = request.POST.get("account_type", "user")  # Default to 'user'

        context = {}

        # Check if user exists in the database
        try:
            user = UserAccount.objects.get(email=email, password=password, user_type=account_type)
            
            # Store user data in session
            request.session["customer_id"] = user.id  # Store user ID
            request.session["account_type"] = user.user_type  # Store user type
            request.session["username"] = user.username # store username in session object
            
            # Redirect based on user type
            if account_type == "admin":
                return redirect("home")
            else:
                return redirect("home")

        except UserAccount.DoesNotExist:
            messages.error(request, "Invalid email, password, or account type!")

    return render(request, "authentication/login.html")


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user_type = request.POST.get("account_type","user")  

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        # Check if email or username already exists
        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("register")

        # Save user info to the database
        user = UserAccount(username=name, email=email, password=password, user_type=user_type)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")  # Redirect to login page

    return render(request, "authentication/register.html")


def admin_register(request):
    return render(request, 'authentication/admin_register.html')