"""my_personal_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
from personal_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("personal_app.urls")),
    path("user/login/", auth_views.LoginView.as_view(), name="user_login"),
    path("user/logout/", auth_views.LogoutView.as_view(), name="user_logout")
]


# Note: We have used CBTs for login and logout in this example.
# We have used "LoginView" and "LogoutView" classes for the login and logout.
# Whenever we use CBTs for login, we should create a template with directory as "registration/login.html".
# Form object called "form" will be created by django.
