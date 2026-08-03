from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Member, Program, Gallery, News, Donation, Expense

def home(request):
    latest_news = News.objects.filter(is_active=True).first()
    committee_members = Member.objects.all()[:4]
    upcoming_programs = Program.objects.filter(is_upcoming=True)[:3]
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
    news_items = News.objects.filter(is_active=True)
    return render(request, 'news.html', {'news_items': news_items})

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
    recent_news = News.objects.filter(is_active=True)[:5]
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
from .forms import DonationForm, ExpenseForm, ProgramForm, MemberForm, MonthlyDonorForm
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
            messages.success(request, 'Donation added successfully!')
            return redirect('manage_donations')
    else:
        form = DonationForm()
    
    donations = Donation.objects.all()
    return render(request, 'manage_donations.html', {'form': form, 'donations': donations})

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
    
    expenses = Expense.objects.all()
    return render(request, 'manage_expenses.html', {'form': form, 'expenses': expenses})

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
    
    programs = Program.objects.all()
    return render(request, 'manage_programs.html', {'form': form, 'programs': programs})
