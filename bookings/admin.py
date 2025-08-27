from django.contrib import admin
from .models import TravelOption, Booking, Profile

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_type','source','destination','date_time','price','available_seats')
    list_filter = ('travel_type','source','destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id','user','travel_option','seats','total_price','status','booking_date')
    list_filter = ('status','booking_date')

admin.site.register(Profile)
