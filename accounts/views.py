from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()


# =========================
# Register View
# =========================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# =========================
# Dashboard View
# =========================
@login_required
def dashboard_view(request):
    user = request.user

    context = {
        'user': user,
    }

    if user.user_type == 'STUDENT':
        return render(request, 'dashboard/student_dashboard.html', context)

    elif user.user_type == 'EMPLOYER':
        return render(request, 'dashboard/employer_dashboard.html', context)

    else:
        return render(request, 'dashboard/admin_dashboard.html', context)



# =========================
# Profile View (NEW)
# =========================
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user
    })


# =========================
# Edit Profile
# =========================
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', user_id=request.user.id)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/edit_profile.html', context)

from django.contrib.auth import get_user_model

User = get_user_model()


def users_list_view(request):
    users = User.objects.all()

    return render(request, 'accounts/users_list.html', {
        'users': users
    })
