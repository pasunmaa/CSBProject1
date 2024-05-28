"""
URL configuration for webApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from webApp.views import (home_view, login_view, logout_view, lockout,
    create_view, list_view, detail_view, update_view, delete_view)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('lockout/', login_view, name='lockout'),
    path('logout/', logout_view, name='logout'),
    path('list/', list_view, name='list_transactions'),
    path('create/', create_view, name='create_new_transaction'),
    path('<id>', detail_view, name='detail_view'),
    path('<id>/update', update_view, name='update_view'),
    path('<id>/delete', delete_view, name='delete_view')
]
