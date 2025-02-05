"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Updated to use the class-based view
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('pay_bills/', views.pay_bills, name='pay_bills'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

