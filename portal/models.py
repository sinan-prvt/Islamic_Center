from django.db import models
from django.utils.translation import gettext_lazy as _

class MonthlyDonor(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    monthly_commitment = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount they agreed to pay each month")
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Member(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='committee/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which they appear on the committee page")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.role}"


class Program(models.Model):
    PROGRAM_TYPES = (
        ('weekly', 'Weekly Dars'),
        ('monthly', 'Monthly Meeting'),
        ('relief', 'Relief Activity'),
        ('class', 'Islamic Class'),
        ('youth', 'Youth Program'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES, default='other')
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    banner = models.ImageField(upload_to='programs/', null=True, blank=True)
    is_upcoming = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_published']
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class Donation(models.Model):
    DONATION_TYPES = (
        ('monthly', 'Monthly Fund'),
        ('general', 'General Donation'),
    )
    donor_name = models.CharField(max_length=255, default='Anonymous')
    monthly_donor = models.ForeignKey(MonthlyDonor, on_delete=models.SET_NULL, null=True, blank=True, help_text="Link this donation to a registered monthly donor")
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.donor_name} - {self.amount} ({self.donation_type})"


class Expense(models.Model):
    EXPENSE_CATEGORIES = (
        ('education', 'Educational Program'),
        ('relief', 'Relief'),
        ('office', 'Office'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.amount}"
