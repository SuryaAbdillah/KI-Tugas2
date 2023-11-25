"""
URL configuration for kampdurirun project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from user.views import index, registration, login_view, logout_view, home_view
from data.views import show_user_data, edit_user_data, add_user_data
from postingans.views import upload_file, success_page, postingans_list, user_postingans, download_key, send_encryption_key_email, download_with_key

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),
    path('registration/', registration, name='registration'),
    path('login/', login_view, name='login'),

    # path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home_view'),

    # Add other paths as needed
    path('show/', show_user_data, name='show_user_data'),
    path('edit/', edit_user_data, name='edit_user_data'),
    path('add/', add_user_data, name='add_user_data'),

    path('upload/', upload_file, name='upload_file'),
    path('success/', success_page, name='success_page'),
    path('list/', postingans_list, name='postingans_list'),
    path('user/', user_postingans, name='user_postingans'),
    path('download-key/<int:postingans_id>/', download_key, name='download_key'),
    path('send-key/<int:postingans_id>/', send_encryption_key_email, name='send_encryption_key_email'),
    path('download-with-key/<int:postingans_id>/', download_with_key, name='download_with_key'),
]