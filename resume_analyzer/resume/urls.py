from django.urls import path
from .views import ResumeDetailView, ResumeUploadView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume_upload'),
    path('<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
]
