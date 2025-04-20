from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Resume
from .serializers import ResumeDetailSerializer, ResumeUploadSerializer
from rest_framework.generics import RetrieveAPIView
import logging

logger = logging.getLogger(__name__)


from .models import Resume
from .serializers import ResumeUploadSerializer

from .tasks import parse_resume_file

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)

            parse_resume_file.delay(resume.id)

            return Response({
                "message": "Resume uploaded successfully. Parsing in background.",
                "resume_id": resume.id
            }, status=status.HTTP_202_ACCEPTED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeDetailView(RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeDetailSerializer
    permission_classes = [IsAuthenticated]

