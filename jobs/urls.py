from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:id>/', views.job_detail, name='job_detail'),
    path('post/', views.post_job, name='post_job'),
    path('admin/approval/', views.admin_job_approval, name='admin_job_approval'),
]
