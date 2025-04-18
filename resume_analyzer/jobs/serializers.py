from rest_framework import serializers
from .models import JobListing

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = ['id', 'title', 'description', 'location', 'experience_required', 'skills_required', 'created_at']
        read_only_fields = ['id', 'created_at']


from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'applicant_email', 'match_score', 'resume_url', 'created_at']

    def get_resume_url(self, obj):
        if obj.resume:
            return obj.resume.url
        return None
