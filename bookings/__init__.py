# bookings/apps.py
from django.apps import AppConfig
import pymysql
class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        import bookings.signals
