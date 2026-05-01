from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.db.models import Sum
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from buildings.models import Building, Unit
from tenants.models import Tenant
from billing.models import Bill, BillingSettings
from core.models import User
from .forms import EmailUserCreationForm, ProfileUpdateForm, PasswordResetRequestForm, CustomSetPasswordForm, EmailAuthenticationForm



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = EmailAuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend='core.backends.EmailOrPhoneBackend')
            messages.success(request, f'Welcome back, {user.name}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email/phone or password.')

    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        print("==================: ", request.POST)
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            BillingSettings.objects.create(user=user)
            login(request, user, backend='core.backends.EmailOrPhoneBackend')
            messages.success(request, 'Account created successfully! Welcome to Propixy.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                print("========================: ", field, errors)
                for error in errors:
                    messages.error(request, error)
    else:
        form = EmailUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user

    buildings = Building.objects.filter(user=user)
    units = Unit.objects.filter(user=user)
    tenants = Tenant.objects.filter(user=user, is_active=True)

    total_buildings = buildings.count()
    total_units = units.count()
    occupied_units = units.filter(status='occupied').count()
    vacant_units = units.filter(status='vacant').count()
    total_tenants = tenants.count()

    expected_rent = units.filter(status='occupied').aggregate(
        total=Sum('monthly_rent')
    )['total'] or 0

    recent_bills = Bill.objects.filter(user=user).order_by('-created_at')[:5]

    occupancy_rate = 0
    if total_units > 0:
        occupancy_rate = round((occupied_units / total_units) * 100, 1)

    building_stats = []
    for building in buildings:
        building_stats.append({
            'name': building.name,
            'total_units': building.total_units,
            'occupied': building.occupied_units,
            'vacant': building.vacant_units,
            'occupancy_rate': building.occupancy_rate,
        })

    context = {
        'total_buildings': total_buildings,
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'total_tenants': total_tenants,
        'expected_rent': expected_rent,
        'occupancy_rate': occupancy_rate,
        'recent_bills': recent_bills,
        'building_stats': building_stats,
    }

    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'core/profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomSetPasswordForm(request.user)

    return render(request, 'core/change_password.html', {'form': form})


def password_reset_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/password-reset-confirm/{uid}/{token}/')

                subject = 'Password Reset Request - Propixy'
                message = f"""
Hi {user.name},

You requested a password reset. Click the link below to reset your password:

{reset_link}

This link will expire in 24 hours.

If you didn't request this, please ignore this email.

Best regards,
Propixy Team
                """
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                messages.success(request, 'Password reset link sent to your email.')
                return redirect('password_reset_done')
            except User.DoesNotExist:
                messages.info(request, 'If an account with that email exists, a reset link has been sent.')
                return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'core/password_reset.html', {'form': form})


def password_reset_done_view(request):
    return render(request, 'core/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset')

    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password has been reset successfully! You can now login.')
            return redirect('password_reset_complete')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomSetPasswordForm(user)

    return render(request, 'core/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})


def password_reset_complete_view(request):
    return render(request, 'core/password_reset_complete.html')