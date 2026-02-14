"""
URL configuration for jobportal project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Home Page
    path('', lambda request: render(request, 'home.html'), name='home'),

    # Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    # App URLs
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('applications/', include('applications.urls')),
    path('messaging/', include('messaging.urls')),
    path('accounts/', include('accounts.urls')),


]

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
