# bookings/urls.py
from django.urls import path
from .views import (TravelListView, TravelDetailView, CreateBookingView,
                    MyBookingsView, CancelBookingView, RegisterView, profile_view,CustomLoginView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TravelListView.as_view(), name='travel_list'),
    path('travel/<int:pk>/', TravelDetailView.as_view(), name='travel_detail'),
    path('travel/<int:pk>/book/', CreateBookingView.as_view(), name='create_booking'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('cancel-booking/<int:pk>/', CancelBookingView.as_view(), name='cancel_booking'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view, name='profile'),
]
