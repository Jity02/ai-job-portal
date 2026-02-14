from django.urls import path
from . import views

urlpatterns = [
    # Registration
    path('register/', views.register_view, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Profile Page (View any user)
    path('profile/<int:user_id>/', views.profile_view, name='profile'),

    # Edit Own Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('users/', views.users_list_view, name='users_list'),

]
