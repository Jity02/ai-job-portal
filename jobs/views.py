from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm


# ==========================================
# JOB LIST
# ==========================================

def job_list(request):
    jobs = Job.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ==========================================
# JOB DETAIL
# ==========================================

def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'jobs/job_detail.html', {'job': job})


# ==========================================
# POST JOB (EMPLOYER)
# ==========================================

@login_required
def post_job(request):

    if request.user.user_type != 'EMPLOYER':
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.is_approved = False
            job.save()

            messages.success(request, "Job posted. Waiting for admin approval.")
            return redirect('dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})


# ==========================================
# ADMIN JOB APPROVAL
# ==========================================

@login_required
def admin_job_approval(request):

    if request.user.user_type != "ADMIN":
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    if request.method == "POST":

        job_id = request.POST.get("job_id")
        action = request.POST.get("action")

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            messages.error(request, "Job not found.")
            return redirect('jobs:admin_job_approval')

        if action == "approve":
            job.is_approved = True
            job.save()
            messages.success(request, "Job approved successfully!")

        elif action == "reject":
            job.delete()
            messages.success(request, "Job rejected successfully!")

        return redirect('jobs:admin_job_approval')

    jobs = Job.objects.filter(is_approved=False).order_by('-created_at')

    return render(request, 'jobs/admin_job_approval.html', {
        'jobs': jobs
    })
