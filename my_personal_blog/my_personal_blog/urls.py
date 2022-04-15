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


# Remember:- urls "127.0.0.1:8000" and "127.0.0.1:8000/" are same. This is the domain name.
# But the urls with endpoints "shiva" and "shiva/" are different.
# urls "127.0.0.1:8000/shiva" and "127.0.0.1:8000/shiva/" are different. They are not the same urls.
# urls "127.0.0.1:8000/{empty string}" and "127.0.0.1:8000/{empty string}/" are different.
# urls "127.0.0.1:8000/hello" and "127.0.0.1:8000/hello/" are different. They take us to different pages.


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("personal_app.urls")),
    path("user/login/", auth_views.LoginView.as_view(), name="user_login"),
    path("user/logout/", auth_views.LogoutView.as_view(), name="user_logout")
]


# We have used "LoginView" and "LogoutView" classes for the login and logout.
# Form object called "form" will be created by django.

# Note:
# If we use "LoginView", then we should create "registration/login.html" template file. It redirects to settings.LOGIN_REDIRECT_URL.
# If we don't want to call the template "registration/login.html", then we should pass the template_name in the "as_view" method in urls.py file.

# If we use "LogoutView", then we should create "registration/logged_out.html" template file. This page is the thank you page. After the logout, user will be redirected to this page.
# If we don't create the template "registration/logged_out.html", then "LogoutView" redirects the user to the home page.
# If we don't want to create the template "registration/logged_out.html", then we can give settings.LOGOUT_REDIRECT_URL to redirect the user.


# Note:- For "login" we need 2 things; they are "login template page" and "redirect page".
# For "logout" we need only 1 thing; just "redirect page"/"thank you page" is enough.

