from django.conf.urls.i18n import urlpatterns
from django.urls import path
from .views import dashboard, profile_list, profile, profile_update
from. import views as user_view
from. import views


app_name = "Naija_X"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path('logout/', user_view.Logout, name ='logout'),
    path('login/', user_view.Login, name ='login'),  
    path('register/', user_view.register, name ='register'),
    path('update_profile/', user_view.profile_update, name ='update_profile'),

] 