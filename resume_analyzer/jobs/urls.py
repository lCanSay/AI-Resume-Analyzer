from django.urls import path
from .views import ApplyToJobView, JobListingCreateView, JobListingDeleteView, JobListingDetailView, JobListingListView, JobSeekerApplicationsView, RecruiterApplicationsView, RecruiterJobListingsView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('create/', JobListingCreateView.as_view(), name='job_create'),
    path('delete/', JobListingDeleteView.as_view(), name='job_delete'),
    path('job-list/', JobListingListView.as_view(), name='job_list'),
    path('job-detail/<int:id>/', JobListingDetailView.as_view(), name='job-detail'),
    path('<int:job_listing_id>/apply/', ApplyToJobView.as_view(), name='job-apply'),
    path('my-jobs/', RecruiterJobListingsView.as_view(), name='my-jobs'),
    path('my-applications/', JobSeekerApplicationsView.as_view(), name='my-applications'),
    path('applications/', RecruiterApplicationsView.as_view(), name='recruiter-applications'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

