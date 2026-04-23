"""
Smart Garbage Complaint System — App URL Configuration

Maps URL patterns to view functions for all complaint-related pages.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ─── Public Pages ─────────────────────────────────────────────────────
    path('', views.home_view, name='home'),
    path('submit/', views.submit_complaint_view, name='submit_complaint'),
    path('success/<str:reference>/', views.success_view, name='complaint_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('complaint/<str:reference>/', views.complaint_detail_view, name='complaint_detail'),
    path('complaint/<str:reference>/update-status/', views.update_status_view, name='update_status'),

    # ─── Authentication ───────────────────────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
