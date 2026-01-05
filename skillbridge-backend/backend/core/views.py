from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import analyze_resume


# =========================
# REGISTER
# =========================
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response(
            {"message": "Registered successfully"},
            status=status.HTTP_201_CREATED
        )


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise Exception()
        except:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        })


# =========================
# RESUME UPLOAD (OPTIONAL)
# =========================
class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        resume = request.FILES.get("resume")

        if not resume:
            return Response(
                {"error": "No resume uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Dummy response (AI later)
        skills = [
            "Python",
            "Django",
            "REST APIs",
            "SQL",
            "Git",
            "Problem Solving"
        ]

        return Response({
            "message": "Resume uploaded successfully",
            "skills": skills
        })


# =========================
# ANALYZE SKILL GAP (CORE)
# =========================
class AnalyzeSkillGapView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        resume = request.FILES.get("resume")
        job_role = request.data.get("job_role")

        if not resume or not job_role:
            return Response(
                {"error": "resume and job_role are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resume_text = resume.read().decode("utf-8", errors="ignore")
            result = analyze_resume(resume_text, job_role)
            return Response(result)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
