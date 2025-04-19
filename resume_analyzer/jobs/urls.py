from django.urls import path
from .views import ApplyToJobView, JobListingCreateView, JobListingDeleteView, JobListingListView

urlpatterns = [
    path('create/', JobListingCreateView.as_view(), name='job_create'),
    path('delete/', JobListingDeleteView.as_view(), name='job_delete'),
    path('job-list/', JobListingListView.as_view(), name='job_list'),
    path('<int:job_listing_id>/apply/', ApplyToJobView.as_view(), name='job-apply'),
]
