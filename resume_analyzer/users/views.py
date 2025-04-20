from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomAuthTokenSerializer, UserRegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class LoginView(APIView):
    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = authenticate(email=email, password=request.data['password'])
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "role": user.role
            })

        return Response(serializer.errors, status=400)
