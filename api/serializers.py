from rest_framework import serializers
from .models import (
    JobPosition,
    JobApplication,
    ProductBuildInquiry,
    HireTalentInquiry,
    AcademyApplication,
    ContactInquiry
)


class JobPositionSerializer(serializers.ModelSerializer):
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    work_type_display = serializers.CharField(source='get_work_type_display', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)

    class Meta:
        model = JobPosition
        fields = [
            'id',
            'title',
            'slug',
            'department',
            'department_display',
            'location',
            'work_type',
            'work_type_display',
            'employment_type',
            'employment_type_display',
            'experience_level',
            'salary_range',
            'summary',
            'description',
            'responsibilities',
            'requirements',
            'benefits',
            'is_active',
            'featured',
            'created_at',
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'position',
            'position_title',
            'role_title_applied',
            'full_name',
            'email',
            'phone',
            'location',
            'years_of_experience',
            'portfolio_url',
            'github_url',
            'linkedin_url',
            'resume',
            'resume_url',
            'cover_note',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, data):
        # Must have at least resume file or resume_url or portfolio/github
        resume = data.get('resume')
        resume_url = data.get('resume_url')
        portfolio_url = data.get('portfolio_url')
        github_url = data.get('github_url')
        linkedin_url = data.get('linkedin_url')

        if not any([resume, resume_url, portfolio_url, github_url, linkedin_url]):
            raise serializers.ValidationError(
                "Please provide a resume file, a resume link, or a portfolio / GitHub / LinkedIn profile."
            )
        return data


class ProductBuildInquirySerializer(serializers.ModelSerializer):
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    budget_range_display = serializers.CharField(source='get_budget_range_display', read_only=True)
    timeline_display = serializers.CharField(source='get_timeline_display', read_only=True)

    class Meta:
        model = ProductBuildInquiry
        fields = [
            'id',
            'full_name',
            'company_name',
            'work_email',
            'phone',
            'project_type',
            'project_type_display',
            'target_platforms',
            'budget_range',
            'budget_range_display',
            'timeline',
            'timeline_display',
            'project_description',
            'existing_spec_url',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']


class HireTalentInquirySerializer(serializers.ModelSerializer):
    engagement_model_display = serializers.CharField(source='get_engagement_model_display', read_only=True)
    seniority_level_display = serializers.CharField(source='get_seniority_level_display', read_only=True)
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)

    class Meta:
        model = HireTalentInquiry
        fields = [
            'id',
            'full_name',
            'company_name',
            'work_email',
            'phone',
            'engagement_model',
            'engagement_model_display',
            'roles_needed',
            'seniority_level',
            'seniority_level_display',
            'headcount',
            'duration',
            'duration_display',
            'start_date',
            'timezone_overlap',
            'technical_requirements',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']


class AcademyApplicationSerializer(serializers.ModelSerializer):
    track_display = serializers.CharField(source='get_track_display', read_only=True)
    experience_level_display = serializers.CharField(source='get_experience_level_display', read_only=True)
    learning_mode_display = serializers.CharField(source='get_learning_mode_display', read_only=True)

    class Meta:
        model = AcademyApplication
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'track',
            'track_display',
            'experience_level',
            'experience_level_display',
            'learning_mode',
            'learning_mode_display',
            'portfolio_or_github',
            'motivation_statement',
            'scholarship_requested',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'subject',
            'message',
            'source',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
