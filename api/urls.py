from django.urls import path
from .views import (
    ApiRootView,
    JobPositionListView,
    JobPositionDetailView,
    JobApplicationCreateView,
    ProductBuildInquiryCreateView,
    HireTalentInquiryCreateView,
    AcademyApplicationCreateView,
    ContactInquiryCreateView
)

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),
    
    # Careers & Job Openings (Specific paths first!)
    path('careers/', JobPositionListView.as_view(), name='careers-list'),
    path('careers/apply/', JobApplicationCreateView.as_view(), name='careers-apply'),
    path('careers/<slug:slug>/', JobPositionDetailView.as_view(), name='careers-detail'),
    
    # Client Inquiries & Specialized Forms
    path('inquiries/product-build/', ProductBuildInquiryCreateView.as_view(), name='inquiry-product-build'),
    path('inquiries/hire-talent/', HireTalentInquiryCreateView.as_view(), name='inquiry-hire-talent'),
    path('inquiries/academy/', AcademyApplicationCreateView.as_view(), name='inquiry-academy'),
    path('inquiries/contact/', ContactInquiryCreateView.as_view(), name='inquiry-contact'),
]
