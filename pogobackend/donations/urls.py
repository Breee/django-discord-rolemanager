
"""pogobackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from pogobackend.settings import MAINTENANCE

urlpatterns = [
    path('', views.me if not MAINTENANCE else views.post_login , name='me'),
    path('me/', views.me if not MAINTENANCE else views.post_login , name='me'),
    path('overview', views.index if not MAINTENANCE else views.post_login , name='home'),
    path('donate/', views.donate if not MAINTENANCE else views.post_login, name='donate'),
    path('pay/', views.pay if not MAINTENANCE else views.post_login, name='pay'),
]

