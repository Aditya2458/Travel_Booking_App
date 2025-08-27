# bookings/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import TravelOption, create_booking, Booking
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta

class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.travel = TravelOption.objects.create(
            travel_type='Bus',
            source='A',
            destination='B',
            date_time=datetime.now() + timedelta(days=1),
            price=Decimal('100.00'),
            available_seats=5
        )

    def test_create_booking_reduces_seats(self):
        booking = create_booking(self.user, self.travel.id, 2)
        self.assertEqual(booking.seats, 2)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 3)

    def test_overbooking_raises(self):
        with self.assertRaises(ValidationError):
            create_booking(self.user, self.travel.id, 10)
