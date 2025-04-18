from rest_framework import serializers
from .models import Resume

class ResumeUploadSerializer(serializers.ModelSerializer):
    parsed_data = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'parsed_data']

    def get_parsed_data(self, obj):
        return obj.parsed_data or {
            "emails": [],
            "phones": [],
            "skills": [],
            "education": [],
            "word_count": 0
        }

class ResumeDetailSerializer(serializers.ModelSerializer):
    parsed_data = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'parsed_data']

    def get_parsed_data(self, obj):
        return obj.parsed_data or {
            "emails": [],
            "phones": [],
            "skills": [],
            "education": [],
            "word_count": 0
        }

