from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import Application
from ats.utils import extract_resume_text, calculate_advanced_ats


# ==========================================
# APPLY FOR JOB
# ==========================================

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    # Only students can apply
    if request.user.user_type != "STUDENT":
        messages.error(request, "Only students can apply for jobs.")
        return redirect('dashboard')

    # Prevent duplicate applications
    if Application.objects.filter(job=job, student=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('jobs:job_detail', id=job.id)

    if request.method == 'POST':

        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, "Please upload your resume.")
            return redirect('applications:apply_job', job_id=job.id)

        # Create application
        application = Application.objects.create(
            job=job,
            student=request.user,
            resume=resume
        )

        # ATS Processing
        try:
            resume_text = extract_resume_text(application.resume.path)
            score = calculate_advanced_ats(resume_text, job.description)
        except Exception:
            score = 0

        application.ats_score = score
        application.save()

        messages.success(
            request,
            f"Application submitted successfully! ATS Score: {score}%"
        )

        return redirect('applications:my_applications')

    return render(request, 'applications/apply_job.html', {'job': job})


# ==========================================
# STUDENT - MY APPLICATIONS
# ==========================================

@login_required
def my_applications(request):

    if request.user.user_type != "STUDENT":
        return redirect('dashboard')

    applications = Application.objects.filter(
        student=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'applications/my_applications.html', {
        'applications': applications
    })


# ==========================================
# EMPLOYER - VIEW APPLICANTS
# ==========================================

@login_required
def employer_applications(request):

    if request.user.user_type != "EMPLOYER":
        return redirect('dashboard')

    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related('job', 'student').order_by('-applied_at')

    return render(request, 'applications/employer_applications.html', {
        'applications': applications
    })
