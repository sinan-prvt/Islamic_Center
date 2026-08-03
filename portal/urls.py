from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('committee/', views.committee, name='committee'),
    path('programs/', views.programs, name='programs'),
    path('gallery/', views.gallery, name='gallery'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    path('monthly-fund/', views.monthly_fund, name='monthly_fund'),
    path('donate/', views.general_donation, name='donate'),
    path('transparency/', views.transparency, name='transparency'),
    path('check-contribution/', views.check_contribution, name='check_contribution'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
