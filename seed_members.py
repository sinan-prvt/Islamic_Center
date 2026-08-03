import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skssf_portal.settings')
django.setup()

from portal.models import Member

# Clear existing members just in case (optional, but let's avoid duplicates)
Member.objects.all().delete()

# Add demo members
demo_members = [
    {'name': 'Sayyid Muhammed Thangal', 'role': 'President', 'phone': '+91 98765 43201'},
    {'name': 'Ustad Abdul Majeed', 'role': 'Vice President', 'phone': '+91 98765 43202'},
    {'name': 'Abdul Rahman', 'role': 'General Secretary', 'phone': '+91 98765 43203'},
    {'name': 'Muhammed Shafi', 'role': 'Joint Secretary', 'phone': '+91 98765 43204'},
    {'name': 'Hassan Musliyar', 'role': 'Treasurer', 'phone': '+91 98765 43205'},
    {'name': 'Fayis Ali', 'role': 'Executive Member', 'phone': '+91 98765 43206'},
    {'name': 'Ashiq Hameed', 'role': 'Executive Member', 'phone': '+91 98765 43207'},
    {'name': 'Yousuf K', 'role': 'Executive Member', 'phone': '+91 98765 43208'},
]

for m in demo_members:
    Member.objects.create(**m)

print("Demo committee members added successfully!")
