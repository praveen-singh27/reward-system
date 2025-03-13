from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import App, Screenshot
from authentication.models import UserAccount

def home(request):
    if request.session.get('customer_id'):
        apps = App.objects.all()
        print(apps)
        return render(request, 'rewards/home.html', {'apps': apps})

    return render(request, 'rewards/home.html')

def logout_view(request):
    request.session.flush()
    logout(request)
    
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def point(request):
    return render(request, 'rewards/points.html')

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

def detail(request, app_id):
    print("App ID:", app_id)
    if request.method == "POST":
        user = UserAccount.objects.get(id=request.session["customer_id"]) 
        print("User ID:", user.id)
        app = App.objects.get(id=request.POST["app_id"])  
        Screenshot.objects.create(
            app=app,
            user=user,
            screenshot=request.FILES["screenshots"]
        )
        
        return redirect("home")

    elif request.session.get('customer_id'):
        app = App.objects.filter(id=app_id).first()
        return render(request, 'rewards/details.html', {'app': app})

    return render(request, 'rewards/details.html')

def profile_view(request):  # Accept user_id from URL
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)
    
    # Get all screenshots uploaded by the user
    screenshots = Screenshot.objects.filter(user=user)
    print("Screenshots: ", screenshots)
    print("Users: ", user)

    # Calculate total points (sum of points from all apps the user has uploaded screenshots for)
    total_points = sum(screenshot.app.points for screenshot in screenshots)

    # Count the number of screenshots as "Tasks Completed"
    tasks_completed = screenshots.count()

    return render(request, 'rewards/profile.html', {'user': user,})

def task_view(request):
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)
    
    # Get all screenshots uploaded by the user (completed tasks)
    screenshots = Screenshot.objects.filter(user=user)
    print("Screenshots: ", screenshots)

    return render(request, 'rewards/tasks.html', {
        'screenshots' : screenshots
    })

def point_view(request):
    user_id = request.session.get('customer_id')
    user = UserAccount.objects.get(id=user_id)
    
    # Get all screenshots uploaded by the user
    screenshots = Screenshot.objects.filter(user=user)
    # Calculate total points (sum of points from all apps the user has uploaded screenshots for)
    total_points = sum(screenshot.app.points for screenshot in screenshots)

    # Count the number of screenshots as "Tasks Completed"
    tasks_completed = screenshots.count()

    return render(request, 'rewards/points.html', {
        
        'total_points': total_points,
        'tasks_completed': tasks_completed,
    })

