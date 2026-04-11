from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/', views.landing_page, name='landing_page'),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('account/register', views.register, name='register'),
    path('account/register/writer', views.register_writer, name='register_as_writer'),
    path('account/login/dashboard', views.login_redriect, name='dashboard')
]