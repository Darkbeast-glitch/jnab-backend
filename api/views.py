from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from .models import (
    JobPosition,
    JobApplication,
    ProductBuildInquiry,
    HireTalentInquiry,
    AcademyApplication,
    ContactInquiry
)
from .serializers import (
    JobPositionSerializer,
    JobApplicationSerializer,
    ProductBuildInquirySerializer,
    HireTalentInquirySerializer,
    AcademyApplicationSerializer,
    ContactInquirySerializer
)


class ApiRootView(views.APIView):
    """
    Overview of all available JNAB Innovations API endpoints.
    """
    def get(self, request):
        return Response({
            "service": "JNAB Innovations Backend API",
            "version": "1.0.0",
            "status": "operational",
            "endpoints": {
                "careers_list": request.build_absolute_uri("/api/careers/"),
                "career_apply": request.build_absolute_uri("/api/careers/apply/"),
                "inquiry_product_build": request.build_absolute_uri("/api/inquiries/product-build/"),
                "inquiry_hire_talent": request.build_absolute_uri("/api/inquiries/hire-talent/"),
                "inquiry_academy": request.build_absolute_uri("/api/inquiries/academy/"),
                "inquiry_contact": request.build_absolute_uri("/api/inquiries/contact/"),
                "admin": request.build_absolute_uri("/admin/"),
            }
        })


# =====================================================================
# CAREERS & TALENT RECRUITMENT APIS
# =====================================================================

class JobPositionListView(generics.ListAPIView):
    """
    GET /api/careers/
    Lists all active career openings at JNAB.
    Supports filtering by ?department=engineering|design|talent|operations
    """
    serializer_class = JobPositionSerializer

    def get_queryset(self):
        queryset = JobPosition.objects.filter(is_active=True)
        department = self.request.query_params.get('department')
        search = self.request.query_params.get('search')
        
        if department and department.lower() != 'all':
            queryset = queryset.filter(department=department.lower())
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(requirements__icontains=search)
            )
        return queryset


class JobPositionDetailView(generics.RetrieveAPIView):
    """
    GET /api/careers/<slug_or_id>/
    Retrieves full details for a specific career opening.
    """
    serializer_class = JobPositionSerializer
    lookup_field = 'slug'

    def get_object(self):
        lookup = self.kwargs.get('slug')
        if lookup.isdigit():
            return generics.get_object_or_404(JobPosition, id=int(lookup), is_active=True)
        return generics.get_object_or_404(JobPosition, slug=lookup, is_active=True)


class JobApplicationCreateView(generics.CreateAPIView):
    """
    POST /api/careers/apply/
    Submits a job application for a specific role or general talent consideration.
    Accepts Multipart form data (with file upload for resume) or JSON.
    """
    serializer_class = JobApplicationSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response({
            "success": True,
            "message": "Thank you for applying to JNAB Innovations. Our talent engineering team will review your profile.",
            "data": JobApplicationSerializer(application).data
        }, status=status.HTTP_201_CREATED)


# =====================================================================
# CLIENT INQUIRY & FORM APIS (PRODUCT BUILD, HIRE TALENT, ACADEMY, CONTACT)
# =====================================================================

class ProductBuildInquiryCreateView(generics.CreateAPIView):
    """
    POST /api/inquiries/product-build/
    Submits a new Full-Cycle Product Build, UI/UX Design, or Software Engineering request.
    """
    serializer_class = ProductBuildInquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = serializer.save()
        return Response({
            "success": True,
            "message": "Your product build inquiry has been received. A JNAB solution architect will contact you within 24 hours.",
            "data": ProductBuildInquirySerializer(inquiry).data
        }, status=status.HTTP_201_CREATED)


class HireTalentInquiryCreateView(generics.CreateAPIView):
    """
    POST /api/inquiries/hire-talent/
    Submits a request to embed senior African developers or deploy an autonomous tech pod.
    """
    serializer_class = HireTalentInquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = serializer.save()
        return Response({
            "success": True,
            "message": "Your talent inquiry has been logged. We will prepare pre-vetted senior candidate profiles tailored to your stack.",
            "data": HireTalentInquirySerializer(inquiry).data
        }, status=status.HTTP_201_CREATED)


class AcademyApplicationCreateView(generics.CreateAPIView):
    """
    POST /api/inquiries/academy/
    Submits an application for JNAB Academy fellowships or enterprise technical upskilling.
    """
    serializer_class = AcademyApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        return Response({
            "success": True,
            "message": "Your JNAB Academy application has been submitted. Check your email for next steps regarding the technical review.",
            "data": AcademyApplicationSerializer(application).data
        }, status=status.HTTP_201_CREATED)


class ContactInquiryCreateView(generics.CreateAPIView):
    """
    POST /api/inquiries/contact/
    General contact form or instant consultation trigger from website banners and footer.
    """
    serializer_class = ContactInquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()
        return Response({
            "success": True,
            "message": "Thank you for reaching out to JNAB. Our team will get back to you promptly.",
            "data": ContactInquirySerializer(contact).data
        }, status=status.HTTP_201_CREATED)
