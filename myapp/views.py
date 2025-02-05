# views.py
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from myapp.forms import RegistrationForm
from .models import Profile
import logging
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib import messages 
from allauth.account.auth_backends import AuthenticationBackend  # Import the backend
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from myapp.models import Transaction
from decimal import Decimal
from django.db import transaction

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')



AuthenticationBackend

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('user_dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user without an email
            user = form.save(commit=False)
            user.email = ""  # Set email to an empty string
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()

            # Log the user in
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'  # Set the backend as a string
            login(request, user)

            # Add a success message after registration
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:

            logger.warning(f"Failed registration attempt: {request.POST.get('username')}")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        
        if user.is_staff:  # Admin user
            logger.info(f"Admin login successful: {user.username}")
            return redirect('admin_dashboard')  # Redirect to the admin panel
        else:  # Normal user
            logger.info(f"User login successful: {user.username}")
            return redirect('user_dashboard')  # Redirect to user dashboard

    def form_invalid(self, form):
        logger.warning("Failed login attempt")
        return self.render_to_response(self.get_context_data(form=form))
       
@login_required
def user_dashboard(request):

    if request.user.is_staff:  # Prevent admins from accessing user dashboard
        raise Http404("Page not found") 
    

    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'user_dashboard.html', {'balance': profile.balance})



@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions.html', {'transactions': user_transactions})


BANK_CHOICES = [
    "ABC Bank", "XYZ Bank", "FastPay Bank", "SecureBank", "FutureBank"
]

@login_required
def transfer_money(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        amount = request.POST.get('amount')

        try:
            sender_profile, _ = Profile.objects.get_or_create(user=request.user)
            amount = Decimal(amount)

            if sender_profile.balance >= amount:
                with transaction.atomic():  # Ensures atomicity
                    sender_profile.balance -= amount
                    sender_profile.save()

                    Transaction.objects.create(
                        user=request.user,
                        description=f"Transfer to {bank_name} - Acc No: {account_number}",
                        amount=-amount,
                        balance_after=sender_profile.balance
                    )

                messages.success(request, f'Transferred ${amount} to {bank_name}, Account No: {account_number}')
            else:
                messages.error(request, 'Insufficient balance')

        except ValueError:
            messages.error(request, 'Invalid amount')

        return redirect('user_dashboard')

    return render(request, 'transfer_money.html', {'banks': BANK_CHOICES})


@login_required
def pay_bills(request):
    if request.method == "POST":
        bill_type = request.POST.get("bill_type")
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)  # Convert amount to Decimal for accuracy
            user_profile, _ = Profile.objects.get_or_create(user=request.user)

            if user_profile.balance >= amount:
                with transaction.atomic():  # Ensures the transaction is completed properly
                    user_profile.balance -= amount
                    user_profile.save()

                    # Record the transaction
                    Transaction.objects.create(
                        user=request.user,
                        description=f"Bill Payment - {bill_type.capitalize()}",
                        amount=-amount,
                        balance_after=user_profile.balance
                    )

                messages.success(request, f"Successfully paid ${amount} for {bill_type} bill.")
            else:
                messages.error(request, "Insufficient balance to pay the bill.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")

        return redirect('user_dashboard')  # Redirect after processing

    return render(request, 'pay_bills.html')


def is_admin(user):
    return user.is_authenticated and user.is_staff  # Restrict access to staff users only

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get all user profiles and their associated roles and balances
    profiles = Profile.objects.filter(user__is_superuser=False)
    total_balance = sum(profile.balance for profile in profiles)
    # Pass the profiles to the template
    context = {
        'profiles': profiles,  # Pass all user profiles to the template
        'total_balance': total_balance,
    }

    return render(request, 'admin_dashboard.html', context)


@require_POST
@user_passes_test(is_admin)
def delete_user(request, username):
    try:
        # Get the user and profile to delete
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        # Delete the profile and user
        profile.delete()  # This will delete the Profile model entry
        user.delete()  # This will delete the User model entry

        # Redirect back to the dashboard
        return redirect('admin_dashboard')
    except (User.DoesNotExist, Profile.DoesNotExist):
        raise Http404("User not found")
    

