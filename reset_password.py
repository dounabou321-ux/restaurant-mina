"""
Script to reset admin password for Mama's Mina restaurant.
Run with: python reset_password.py
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mama_mina.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = input("Enter username to reset password: ")

try:
    user = User.objects.get(username=username)
    new_password = input("Enter new password: ")
    new_password_confirm = input("Confirm new password: ")
    
    if new_password != new_password_confirm:
        print("Error: Passwords don't match!")
    else:
        user.set_password(new_password)
        user.save()
        print(f"Password for '{username}' has been reset successfully!")
except User.DoesNotExist:
    print(f"Error: User '{username}' does not exist!")
