"""
Script to create an admin superuser for Mama's Mina restaurant.
Run with: python create_admin.py
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mama_mina.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = input("Enter username: ")
email = input("Enter email (optional, press Enter to skip): ")
password = input("Enter password: ")
password_confirm = input("Confirm password: ")

if password != password_confirm:
    print("Error: Passwords don't match!")
else:
    if User.objects.filter(username=username).exists():
        print(f"Error: User '{username}' already exists!")
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email if email else None,
            password=password
        )
        print(f"Superuser '{username}' created successfully!")
        print(f"You can now login at /admin/ or /accounts/login/")
