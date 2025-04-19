from rest_framework import generics, permissions, status

from .utils import calculate_match_score
from .serializers import JobListingSerializer
from .models import Application, Resume, JobListing
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JobListingSerializer, ApplicationSerializer


import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_md")


class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'recruiter'

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



class ApplyToJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_listing_id):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can apply to jobs."}, status=status.HTTP_403_FORBIDDEN)

        job_listing = get_object_or_404(JobListing, id=job_listing_id)

        resume = Resume.objects.filter(user=request.user).order_by('-uploaded_at').first()
        if not resume:
            return Response({"error": "No resume found."}, status=status.HTTP_400_BAD_REQUEST)

        parsed_skills = [skill.lower() for skill in resume.parsed_data.get('skills', [])]
        required_skills = [skill.lower() for skill in (job_listing.skills_required or [])]

        if not parsed_skills:
            return Response({"error": "No parsed skills found in resume."}, status=status.HTTP_400_BAD_REQUEST)

        matched_skills = set(parsed_skills) & set(required_skills)
        missing_skills = set(required_skills) - matched_skills

        skill_score = (len(matched_skills) / max(len(required_skills), 1)) * 7.0

        job_text = f"{job_listing.title} {job_listing.description} {' '.join(job_listing.skills_required)}"
        resume_text = resume.parsed_data.get('text', '')
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_text.lower())
        general_score = resume_doc.similarity(job_doc) * 3.0

        total_score = round(skill_score + general_score, 1)
        total_score = min(total_score, 9.5)

        if missing_skills:
            suggestions = f"To improve your chances, consider learning: {', '.join(missing_skills)}."
        else:
            suggestions = "You match all required skills!"

        application = Application.objects.create(
            applicant=request.user,
            job_listing=job_listing,
            resume=resume.file,
            match_score=int(total_score)
        )

        serializer = ApplicationSerializer(application)
        return Response({
            "match_score": total_score,
            "suggestions": suggestions,
            "application": serializer.data
        }, status=status.HTTP_201_CREATED)
    
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
    
class RecruiterApplicationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can view applications."}, status=status.HTTP_403_FORBIDDEN)

        job_id = request.query_params.get('job_id')
        applications = Application.objects.filter(job_listing__recruiter=request.user)
        if job_id:
            applications = applications.filter(job_listing__id=job_id)

        applications = applications.order_by('-match_score')

        data = [
            {
                'job_title': app.job_listing.title,
                'applicant_email': app.applicant.email,
                'resume_url': app.resume.url if app.resume else None,
                'match_score': app.match_score,
                'applied_at': app.created_at
            }
            for app in applications
        ]

        return Response(data)

class JobSeekerApplicationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can view their applications."}, status=status.HTTP_403_FORBIDDEN)

        applications = Application.objects.filter(applicant=request.user).order_by('-created_at')

        data = [
            {
                'job_title': app.job_listing.title,
                'company': app.job_listing.company,
                'resume_url': app.resume.url if app.resume else None,
                'match_score': app.match_score,
                'applied_at': app.created_at
            }
            for app in applications
        ]

        return Response(data)
