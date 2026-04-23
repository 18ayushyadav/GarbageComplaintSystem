"""
Smart Garbage Complaint System — Views

All view functions for the application:
- home_view: Landing page with live statistics
- submit_complaint_view: Form for submitting complaints + email notification
- success_view: Confirmation page after submission
- dashboard_view: Filterable list of all complaints
- complaint_detail_view: Single complaint view + status update
- update_status_view: AJAX/POST endpoint for staff status updates
- register_view / login_view / logout_view: Authentication
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse

from .models import Complaint
from .forms import ComplaintForm, UserRegisterForm
from .utils import send_complaint_notification, send_status_update_email


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

def home_view(request):
    """
    Landing page with hero section and live complaint statistics.

    Displays:
    - Total complaints filed
    - Pending complaints count
    - Resolved complaints count
    - In-progress complaints count

    This gives visitors immediate insight into system activity.
    """
    stats = Complaint.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        resolved=Count('id', filter=Q(status='resolved')),
    )

    context = {
        'stats': stats,
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)


def submit_complaint_view(request):
    """
    Handle complaint submission.

    GET: Display the complaint form
    POST: Validate, save complaint, send email notification, redirect to success

    If user is authenticated, the complaint is automatically linked to
    their account and reporter fields are pre-filled.
    """
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)

            # Link to user account if logged in
            if request.user.is_authenticated:
                complaint.user = request.user

            complaint.save()

            # Send email notification to municipal authority
            email_sent = send_complaint_notification(complaint)

            if email_sent:
                messages.success(
                    request,
                    f'✅ Complaint submitted successfully! Reference: {complaint.reference_number}. '
                    f'Email notification sent to municipal authority.'
                )
            else:
                messages.success(
                    request,
                    f'✅ Complaint submitted! Reference: {complaint.reference_number}. '
                    f'(Email notification could not be sent, but your complaint is recorded.)'
                )

            # Redirect to success page with the complaint reference
            return redirect('complaint_success', reference=complaint.reference_number)
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        # Pre-fill form for authenticated users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'reporter_name': request.user.get_full_name() or request.user.username,
                'reporter_email': request.user.email,
            }
        form = ComplaintForm(initial=initial_data)

    context = {
        'form': form,
        'page_title': 'Submit Complaint',
    }
    return render(request, 'submit_complaint.html', context)


def success_view(request, reference):
    """
    Display a success confirmation page after complaint submission.

    Shows the complaint reference number and next steps.
    """
    complaint = get_object_or_404(Complaint, reference_number=reference)
    context = {
        'complaint': complaint,
        'page_title': 'Complaint Submitted',
    }
    return render(request, 'success.html', context)


def dashboard_view(request):
    """
    Dashboard showing all complaints with search and filter capabilities.

    Supports:
    - Search by location, description, or reference number
    - Filter by status (pending, in_progress, resolved)
    - Filter by priority (low, medium, high, critical)
    - Sorted by newest first (default)
    """
    complaints = Complaint.objects.all()

    # ─── Search ───────────────────────────────────────────────────────────
    search_query = request.GET.get('search', '').strip()
    if search_query:
        complaints = complaints.filter(
            Q(location_text__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(reference_number__icontains=search_query) |
            Q(reporter_name__icontains=search_query)
        )

    # ─── Filters ──────────────────────────────────────────────────────────
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    priority_filter = request.GET.get('priority', '').strip()
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)

    # ─── Statistics for dashboard header ──────────────────────────────────
    all_complaints = Complaint.objects.all()
    stats = all_complaints.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        resolved=Count('id', filter=Q(status='resolved')),
    )

    context = {
        'complaints': complaints,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)


def complaint_detail_view(request, reference):
    """
    Display full details of a single complaint.

    Staff users can update the complaint status and add admin remarks.
    Regular users can only view their complaint details.
    """
    complaint = get_object_or_404(Complaint, reference_number=reference)

    context = {
        'complaint': complaint,
        'page_title': f'Complaint {complaint.reference_number}',
    }
    return render(request, 'complaint_detail.html', context)


def update_status_view(request, reference):
    """
    Update the status of a complaint (staff-only action).

    This endpoint handles POST requests from the complaint detail page
    to update a complaint's status and admin remarks.
    """
    if not request.user.is_staff:
        messages.error(request, '⛔ You do not have permission to update complaint status.')
        return redirect('complaint_detail', reference=reference)

    complaint = get_object_or_404(Complaint, reference_number=reference)
    old_status = complaint.status

    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_remarks = request.POST.get('admin_remarks', '')

        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.admin_remarks = admin_remarks
            complaint.save()

            # Send status update email to the complainant
            if old_status != new_status:
                send_status_update_email(complaint)

            messages.success(
                request,
                f'✅ Status updated to "{complaint.get_status_display()}" for {complaint.reference_number}'
            )
        else:
            messages.error(request, '❌ Invalid status value.')

    return redirect('complaint_detail', reference=reference)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTHENTICATION VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

def register_view(request):
    """
    User registration page.

    Creates a new user account and logs them in immediately.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'register.html', context)


def login_view(request):
    """
    User login page.

    Authenticates using Django's built-in authentication system.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.first_name or user.username}!')
            # Redirect to 'next' parameter if provided, otherwise home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, '❌ Invalid username or password.')

    context = {
        'page_title': 'Login',
    }
    return render(request, 'login.html', context)


def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    messages.info(request, '👋 You have been logged out.')
    return redirect('home')
