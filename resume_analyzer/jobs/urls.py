from django.urls import path
from .views import JobListingCreateView, JobListingDeleteView, JobListingListView

urlpatterns = [
    path('create/', JobListingCreateView.as_view(), name='job_create'),
    path('delete/', JobListingDeleteView.as_view(), name='job_delete'),
    path('job-list/', JobListingListView.as_view(), name='job_list'),
]
