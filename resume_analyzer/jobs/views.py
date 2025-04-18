from requests import Response
from rest_framework import generics, permissions

from .utils import calculate_match_score
from .serializers import JobListingSerializer
from .models import Application, Resume, JobListing
from .serializers import ApplicationSerializer
from django.shortcuts import get_object_or_404

class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_recruiter

class IsRecruiterOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.recruiter == request.user

class JobListingCreateView(generics.CreateAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class RecruiterApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'recruiter':
            return Application.objects.none()
        return Application.objects.filter(job_listing__recruiter=user)


class JobListingListView(generics.ListAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.AllowAny]

class JobListingDeleteView(generics.DestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter, IsRecruiterOwner]



class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        job_listing_id = self.kwargs.get('job_listing_id')
        job_listing = get_object_or_404(JobListing, id=job_listing_id)

        resume = Resume.objects.filter(user=request.user).order_by('-uploaded_at').first()
        if not resume:
            return Response({"error": "No resume found."}, status=400)

        required_skills = set(job_listing.required_skills or [])
        applicant_skills = set(resume.parsed_data.get('skills', []))

        if not required_skills:
            match_score = 0
        else:
            match_score = int((len(required_skills & applicant_skills) / len(required_skills)) * 10)

        application = Application.objects.create(
            applicant=request.user,
            job_listing=job_listing,
            resume=resume.file,
            match_score=match_score
        )

        serializer = self.get_serializer(application)
        return Response(serializer.data)

class TopMatchingCandidatesView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request, job_listing_id):
        job_listing = get_object_or_404(JobListing, id=job_listing_id, recruiter=request.user)

        resumes = Resume.objects.all()
        candidates = []

        for resume in resumes:
            applicant_skills = resume.parsed_data.get('skills', [])
            score = calculate_match_score(job_listing.skills_required, applicant_skills)

            candidates.append({
                "resume_id": resume.id,
                "file_url": request.build_absolute_uri(resume.file.url),
                "match_score": score,
                "skills": applicant_skills
            })

        candidates = sorted(candidates, key=lambda x: x['match_score'], reverse=True)
        return Response(candidates)