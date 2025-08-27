from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from decimal import Decimal

# ---------------------------
# PROFILE MODEL
# ---------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

# ---------------------------
# TRAVEL OPTION MODEL
# ---------------------------
class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    ]
    id = models.AutoField(primary_key=True)
    travel_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=9, decimal_places=2)  # e.g., 9999999.99
    available_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.travel_type} {self.source} → {self.destination} on {self.date_time}"

# ---------------------------
# BOOKING MODEL
# ---------------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    id = models.AutoField(primary_key=True)
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username}"

    # ---------------------------
    # MODEL-LEVEL VALIDATION
    # ---------------------------
    def clean(self):
        # Ensure required fields are set
        if self.seats is None:
            raise ValidationError("Number of seats must be provided.")
        if self.seats <= 0:
            raise ValidationError("Number of seats must be a positive integer.")
        if self.travel_option is None:
            raise ValidationError("A travel option must be selected.")
        if self.travel_option.available_seats is None:
            raise ValidationError("Travel option must have available seats set.")
        if self.seats > self.travel_option.available_seats:
            raise ValidationError(
                f"Cannot book {self.seats} seats. Only {self.travel_option.available_seats} available."
            )

    # ---------------------------
    # OVERRIDE SAVE TO RUN VALIDATION
    # ---------------------------
    def save(self, *args, **kwargs):
        self.clean()  # run validations
        super().save(*args, **kwargs)


# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def create_booking(user, travel_option_id, seats):
    """
    Create a booking transactionally and safely.
    """
    if seats is None or seats <= 0:
        raise ValidationError("Seats must be a positive number.")

    with transaction.atomic():
        # Lock the travel option row for safe concurrent updates
        try:
            travel = TravelOption.objects.select_for_update().get(pk=travel_option_id)
        except TravelOption.DoesNotExist:
            raise ValidationError("Travel option does not exist.")

        if travel.available_seats is None:
            raise ValidationError("Travel option seat availability is not set.")

        if travel.available_seats < seats:
            raise ValidationError(
                f"Cannot book {seats} seats. Only {travel.available_seats} available."
            )

        # Calculate total price
        total = (travel.price * Decimal(seats)).quantize(Decimal('0.01'))

        # Reduce available seats
        travel.available_seats -= seats
        travel.save()

        # Create booking
        booking = Booking.objects.create(
            user=user,
            travel_option=travel,
            seats=seats,
            total_price=total,
            status='CONFIRMED'
        )

        return booking


def cancel_booking(booking_pk, user):
    """
    Cancel a booking transactionally and restore seats.
    """
    with transaction.atomic():
        try:
            booking = Booking.objects.select_for_update().get(pk=booking_pk, user=user)
        except Booking.DoesNotExist:
            raise ValidationError("Booking not found.")

        if booking.status != 'CONFIRMED':
            raise ValidationError("Booking is already cancelled.")

        booking.status = 'CANCELLED'

        # Restore seats
        travel = booking.travel_option
        if travel.available_seats is None:
            travel.available_seats = 0
        travel.available_seats += booking.seats
        travel.save()

        booking.save()
        return booking
