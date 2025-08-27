# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TravelOption, Booking, create_booking, cancel_booking
from .forms import BookingForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView

class TravelListView(ListView):
    model = TravelOption
    template_name = 'travel_list.html'
    context_object_name = 'travels'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('date_time')
        ttype = self.request.GET.get('type')
        source = self.request.GET.get('source')
        destination = self.request.GET.get('destination')
        date = self.request.GET.get('date')  # expected YYYY-MM-DD
        if ttype:
            qs = qs.filter(travel_type=ttype)
        if source:
            qs = qs.filter(source__icontains=source)
        if destination:
            qs = qs.filter(destination__icontains=destination)
        if date:
            qs = qs.filter(date_time__date=date)
        return qs

class TravelDetailView(DetailView):
    model = TravelOption
    template_name = 'travel_detail.html'
    context_object_name = 'travel'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = BookingForm()
        return ctx

class CreateBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = BookingForm(request.POST)
        travel = get_object_or_404(TravelOption, pk=pk)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            try:
                booking = create_booking(request.user, travel.id, seats)
                messages.success(request, f"Booking confirmed! Booking ID: {booking.booking_id}")
                return redirect('my_bookings')
            except ValidationError as e:
                form.add_error('seats', e.messages)
            except Exception as e:
                form.add_error(None, "An error occurred. Try again.")
        return render(request, 'travel_detail.html', {'travel': travel, 'form': form})

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            cancel_booking(pk, request.user)
            messages.success(request, "Booking cancelled.")
        except ValidationError as e:
            messages.error(request, e.messages[0])
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")
        return redirect('my_bookings')

# Registration & profile update:
from django.views import generic
class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        valid = super().form_valid(form)
        messages.success(self.request, "Registration successful. You can log in now.")
        return valid

from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        # Always render login page regardless of authentication
        return super().dispatch(request, *args, **kwargs)