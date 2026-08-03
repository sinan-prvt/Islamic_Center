from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Member, Program, Gallery, Donation, Expense, MonthlyDonor

def home(request):
    latest_news = Program.objects.filter(program_type='news').first()
    committee_members = Member.objects.all()[:4]
    upcoming_programs = Program.objects.filter(is_upcoming=True).exclude(program_type='news').order_by('date')[:3]
    recent_donations = Donation.objects.filter(is_public=True)[:5]
    
    income = sum(d.amount for d in Donation.objects.all())
    expenses = sum(e.amount for e in Expense.objects.all())

    context = {
        'latest_news': latest_news,
        'committee_members': committee_members,
        'upcoming_programs': upcoming_programs,
        'recent_donations': recent_donations,
        'total_income': income,
        'total_expenses': expenses,
        'balance': income - expenses,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def committee(request):
    members = Member.objects.all()
    return render(request, 'committee.html', {'members': members})

def programs(request):
    upcoming = Program.objects.filter(is_upcoming=True)
    past = Program.objects.filter(is_upcoming=False)
    return render(request, 'programs.html', {'upcoming': upcoming, 'past': past})

def gallery(request):
    images = Gallery.objects.all().order_by('-date_uploaded')
    return render(request, 'gallery.html', {'images': images})

def news(request):
    news_items = Program.objects.filter(program_type='news')
    events = Program.objects.filter(is_upcoming=True).exclude(program_type='news').order_by('date')
    return render(request, 'news.html', {'news_items': news_items, 'events': events})

def program_detail(request, pk):
    from django.shortcuts import get_object_or_404
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'program_detail.html', {'program': program})

def contact(request):
    return render(request, 'contact.html')

def monthly_fund(request):
    # Dummy target for demo
    target = 15000
    collected = sum(d.amount for d in Donation.objects.filter(donation_type='monthly'))
    remaining = target - collected if target > collected else 0
    progress = (collected / target * 100) if target > 0 else 0
    progress = min(progress, 100) # Cap at 100%

    context = {
        'target': target,
        'collected': collected,
        'remaining': remaining,
        'progress': progress,
    }
    return render(request, 'monthly_fund.html', context)

from django.http import JsonResponse

def check_contribution(request):
    name = request.GET.get('name', '').strip()
    phone = request.GET.get('phone', '').strip()
    
    if not name or not phone:
        return JsonResponse({'error': 'Please provide both name and phone number'}, status=400)
        
    donor = MonthlyDonor.objects.filter(phone=phone).first()
    
    if donor:
        donations = Donation.objects.filter(monthly_donor=donor, donation_type='monthly')
        total_paid = sum(d.amount for d in donations)
        return JsonResponse({
            'is_registered': True,
            'name': donor.name,
            'commitment': str(donor.monthly_commitment),
            'total_paid': str(total_paid),
            'count': donations.count()
        })
    else:
        # Fallback to general search if not a registered monthly donor
        donations = Donation.objects.filter(donor_name__icontains=name, donation_type='monthly')
        total_paid = sum(d.amount for d in donations)
        return JsonResponse({
            'is_registered': False,
            'name': name,
            'total_paid': str(total_paid),
            'count': donations.count()
        })

def general_donation(request):
    # Transparency Data
    monthly_income = sum(d.amount for d in Donation.objects.filter(donation_type='monthly'))
    general_income = sum(d.amount for d in Donation.objects.filter(donation_type='general'))
    total_income = monthly_income + general_income
    
    expenses_list = Expense.objects.all()
    total_expenses = sum(e.amount for e in expenses_list)
    balance = total_income - total_expenses

    recent_donations = Donation.objects.filter(is_public=True).order_by('-date')[:10]
    recent_expenses = expenses_list.order_by('-date')[:10]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_donations': recent_donations,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'general_donation.html', context)

def transparency(request):
    monthly_income = sum(d.amount for d in Donation.objects.filter(donation_type='monthly'))
    general_income = sum(d.amount for d in Donation.objects.filter(donation_type='general'))
    total_income = monthly_income + general_income
    
    expenses = Expense.objects.all()
    total_expenses = sum(e.amount for e in expenses)
    balance = total_income - total_expenses

    context = {
        'monthly_income': monthly_income,
        'general_income': general_income,
        'total_income': total_income,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'balance': balance,
    }
    return render(request, 'transparency.html', context)

@login_required(login_url='/login/')
def dashboard(request):
    # Financial Stats
    monthly_income = sum(d.amount for d in Donation.objects.filter(donation_type='monthly'))
    general_income = sum(d.amount for d in Donation.objects.filter(donation_type='general'))
    total_income = monthly_income + general_income
    
    expenses = Expense.objects.all()
    total_expenses = sum(e.amount for e in expenses)
    balance = total_income - total_expenses

    # General Stats
    member_count = Member.objects.count()
    program_count = Program.objects.count()

    # Recent Activity
    recent_programs = Program.objects.all()[:5]
    recent_news = Program.objects.filter(program_type='news')[:5]
    recent_donations = Donation.objects.filter(is_public=True)[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'member_count': member_count,
        'program_count': program_count,
        'recent_programs': recent_programs,
        'recent_news': recent_news,
        'recent_donations': recent_donations,
        # Pass JSON data for Chart.js
        'chart_data': {
            'income': float(total_income),
            'expenses': float(total_expenses),
            'balance': float(balance)
        }
    }
    return render(request, 'dashboard.html', context)

from django.contrib.admin.views.decorators import staff_member_required
from .forms import DonationForm, ExpenseForm, ProgramForm, MemberForm, MonthlyDonorForm, GalleryForm
from django.contrib import messages
from .models import MonthlyDonor

@staff_member_required(login_url='/login/')
def manage_monthly_donors(request):
    if request.method == 'POST':
        form = MonthlyDonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monthly donor registered successfully!')
            return redirect('manage_monthly_donors')
    else:
        form = MonthlyDonorForm()
    
    donors = MonthlyDonor.objects.all().order_by('-join_date')
    return render(request, 'manage_monthly_donors.html', {'form': form, 'donors': donors})

@staff_member_required(login_url='/login/')
def edit_monthly_donor(request, pk):
    from django.shortcuts import get_object_or_404
    donor = get_object_or_404(MonthlyDonor, pk=pk)
    if request.method == 'POST':
        form = MonthlyDonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monthly donor updated successfully!')
            return redirect('manage_monthly_donors')
    else:
        form = MonthlyDonorForm(instance=donor)
    return render(request, 'edit_monthly_donor.html', {'form': form, 'donor': donor})

@staff_member_required(login_url='/login/')
def delete_monthly_donor(request, pk):
    from django.shortcuts import get_object_or_404
    donor = get_object_or_404(MonthlyDonor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Monthly donor deleted successfully!')
        return redirect('manage_monthly_donors')
    return render(request, 'confirm_delete.html', {'object_name': donor.name, 'cancel_url': 'manage_monthly_donors'})

@staff_member_required(login_url='/login/')
def manage_members(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('manage_members')
    else:
        form = MemberForm()
    
    members = Member.objects.all()
    return render(request, 'manage_members.html', {'form': form, 'members': members})

@staff_member_required(login_url='/login/')
def manage_donations(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation recorded successfully!')
            return redirect('manage_donations')
    else:
        form = DonationForm()
    
    donations = Donation.objects.all().order_by('-date')
    return render(request, 'manage_donations.html', {'form': form, 'donations': donations})

@staff_member_required(login_url='/login/')
def edit_donation(request, pk):
    from django.shortcuts import get_object_or_404
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated successfully!')
            return redirect('manage_donations')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'edit_donation.html', {'form': form, 'donation': donation})

@staff_member_required(login_url='/login/')
def delete_donation(request, pk):
    from django.shortcuts import get_object_or_404
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted successfully!')
        return redirect('manage_donations')
    return render(request, 'confirm_delete.html', {'object_name': f"{donation.donor_name}'s Donation of ₹{donation.amount}", 'cancel_url': 'manage_donations'})

@staff_member_required(login_url='/login/')
def manage_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense logged successfully!')
            return redirect('manage_expenses')
    else:
        form = ExpenseForm()
    
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'manage_expenses.html', {'form': form, 'expenses': expenses})

@staff_member_required(login_url='/login/')
def edit_expense(request, pk):
    from django.shortcuts import get_object_or_404
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('manage_expenses')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})

@staff_member_required(login_url='/login/')
def delete_expense(request, pk):
    from django.shortcuts import get_object_or_404
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('manage_expenses')
    return render(request, 'confirm_delete.html', {'object_name': f"Expense: {expense.title} (₹{expense.amount})", 'cancel_url': 'manage_expenses'})

@staff_member_required(login_url='/login/')
def manage_programs(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program created successfully!')
            return redirect('manage_programs')
    else:
        form = ProgramForm()
    
    programs = Program.objects.all().order_by('-date')
    return render(request, 'manage_programs.html', {'form': form, 'programs': programs})

@staff_member_required(login_url='/login/')
def edit_program(request, pk):
    from django.shortcuts import get_object_or_404
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!')
            return redirect('manage_programs')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'edit_program.html', {'form': form, 'program': program})

@staff_member_required(login_url='/login/')
def delete_program(request, pk):
    from django.shortcuts import get_object_or_404
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('manage_programs')
    return render(request, 'confirm_delete.html', {'object_name': program.title, 'cancel_url': 'manage_programs'})

@staff_member_required(login_url='/login/')
def manage_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('manage_gallery')
    else:
        form = GalleryForm()
    
    images = Gallery.objects.all().order_by('-date_uploaded')
    return render(request, 'manage_gallery.html', {'form': form, 'images': images})

@staff_member_required(login_url='/login/')
def edit_gallery(request, pk):
    from django.shortcuts import get_object_or_404
    image = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!')
            return redirect('manage_gallery')
    else:
        form = GalleryForm(instance=image)
    return render(request, 'edit_gallery.html', {'form': form, 'image': image})

@staff_member_required(login_url='/login/')
def delete_gallery(request, pk):
    from django.shortcuts import get_object_or_404
    image = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('manage_gallery')
    return render(request, 'confirm_delete.html', {'object_name': image.title, 'cancel_url': 'manage_gallery'})
