# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile

@receiver(user_logged_in)
def update_last_active(sender, request, user, **kwargs):
    # Update last_active timestamp when the user logs in
    profile, created = Profile.objects.get_or_create(user=user)
    profile.last_active = user.last_login
    profile.save()
