from django.urls import path
from . import views


urlpatterns = [
    path('logout', views.logout_view, name='logout'),
    path('point', views.point_view, name='point'),
    path('add-app', views.add_app, name='add-app'),
    path('home', views.home, name='home'),
    path('detail/<int:app_id>/', views.detail, name='detail'),
    path('profile', views.profile_view, name='profile'),
    path('task', views.task_view, name='task'),
    path('approval', views.approval_view, name='approval')

] 

