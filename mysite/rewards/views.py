from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import App, Screenshot
from authentication.models import UserAccount

# Home view to display the list of apps
def home(request):
    if request.session.get('customer_id'):
        # Retrieve all apps from the database
        apps = App.objects.all()
        print(apps)
        return render(request, 'rewards/home.html', {'apps': apps})
    
    # If the user is not logged in, render the home page without apps
    return render(request, 'rewards/home.html')

def logout_view(request):
    request.session.flush()
    logout(request)
    
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

# Point view to display points
def point(request):
    return render(request, 'rewards/points.html')

# View to add a new app or update an existing app
def add_app(request):
    app = None 

    if request.method == "POST":
        name = request.POST.get("name")
        link = request.POST.get("link")
        category = request.POST.get("category")
        subcategory = request.POST.get("subcategory")
        points = int(request.POST.get("points", 0))  # Converting  to  integer
        logo = request.FILES.get("logo")

        # Check if an app with the same name AND link exists
        app = App.objects.filter(appname=name, link=link).first()

        if app:
            # Update existing app
            app.category = category
            app.subcategory = subcategory
            app.points = points
            if logo:
                app.logo = logo  # Update logo only if provided
            app.save()
        else:
            # Create new app
            app = App.objects.create(
                appname=name,
                link=link,
                category=category,
                subcategory=subcategory,
                points=points,
                logo=logo
            )

        return redirect("home")

    return render(request, "rewards/add_app.html")

# View to display app detail and upload screenshots
def detail(request, app_id):
    print("App ID:", app_id)
    if request.method == "POST" :
        user = UserAccount.objects.get(id=request.session["customer_id"]) 
        print("User ID:", user.id)

        app = App.objects.get(id=request.POST["app_id"]) 

        Screenshot.objects.create(
            app=app,
            user=user,
            screenshot=request.FILES["screenshots"],
            status="pending"  # Default status is pending
        )
        
        return redirect("home")

    elif request.session.get('customer_id'):
        app = App.objects.filter(id=app_id).first()
        return render(request, 'rewards/details.html', {'app': app})

    return render(request, 'rewards/details.html')

# View to display user profile
def profile_view(request):  # Accept user_id from URL
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)

    return render(request, 'rewards/profile.html', {'user': user,})


# View to display tasks uploaded by the user
def task_view(request):
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)
    
    # Get all screenshots uploaded by the user
    approved_screenshots  = Screenshot.objects.filter(user=user, status="approved")

    # Get pending screenshots (for user info)
    pending_screenshots = Screenshot.objects.filter(user=user, status="pending")

    # Calculate total points (sum of points from all apps the user has uploaded screenshots for)
    total_points = sum(screenshot.app.points for screenshot in approved_screenshots)

    # Get all screenshots uploaded by the user (completed tasks)
    screenshots = Screenshot.objects.filter(user=user)
    print("Screenshots: ", screenshots)

    return render(request, 'rewards/tasks.html', {
        'user': user,
        'total_points': total_points,
        'approved_screenshots': approved_screenshots,
        'pending_screenshots': pending_screenshots,
    })

# View to display points details and tasks completed
def point_view(request):
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)
    
    # Get all screenshots uploaded by the user
    approved_screenshots  = Screenshot.objects.filter(user=user, status="approved")
    # Calculate total points (sum of points from all apps the user has uploaded screenshots for)
    total_points = sum(screenshot.app.points for screenshot in approved_screenshots)

    # Count the number of screenshots as "Tasks Completed"
    tasks_completed = approved_screenshots.count()

    return render(request, 'rewards/points.html', {
        
        'total_points': total_points,
        'tasks_completed': tasks_completed,
    })

