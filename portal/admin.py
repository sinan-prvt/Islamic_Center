from django.contrib import admin
from .models import Member, Program, Gallery, Donation, Expense

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'program_type', 'date', 'is_upcoming')
    list_filter = ('program_type', 'is_upcoming', 'date')
    search_fields = ('title', 'venue')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'date_uploaded')
    list_filter = ('date_uploaded',)
    search_fields = ('title',)



@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'donation_type', 'amount', 'date', 'is_public')
    list_filter = ('donation_type', 'date', 'is_public')
    search_fields = ('donor_name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'amount', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title',)
