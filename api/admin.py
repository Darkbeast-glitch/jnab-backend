from django.contrib import admin
from django.utils.html import format_html
from .models import (
    JobPosition,
    JobApplication,
    ProductBuildInquiry,
    HireTalentInquiry,
    AcademyApplication,
    ContactInquiry
)


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'work_type', 'employment_type', 'experience_level', 'is_active', 'featured', 'created_at']
    list_filter = ['department', 'work_type', 'employment_type', 'is_active', 'featured']
    search_fields = ['title', 'summary', 'requirements', 'responsibilities']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    actions = ['make_active', 'make_inactive', 'make_featured', 'unmake_featured']
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "department", "is_active", "featured")
        }),
        ("Position Parameters", {
            "fields": ("location", "work_type", "employment_type", "experience_level", "salary_range")
        }),
        ("Role Details & Narrative", {
            "fields": ("summary", "description", "responsibilities", "requirements", "benefits")
        }),
    )

    @admin.action(description="Mark selected positions as Active")
    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} position(s) marked as active.")

    @admin.action(description="Mark selected positions as Inactive")
    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} position(s) marked as inactive.")

    @admin.action(description="Mark selected positions as Featured")
    def make_featured(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f"{count} position(s) marked as featured.")

    @admin.action(description="Remove Featured status from selected")
    def unmake_featured(self, request, queryset):
        count = queryset.update(featured=False)
        self.message_user(request, f"{count} position(s) un-featured.")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'get_target_role', 'email', 'phone', 'location', 'years_of_experience', 'status', 'resume_link', 'created_at']
    list_filter = ['status', 'position', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'location', 'cover_note', 'role_title_applied']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

    def get_target_role(self, obj):
        return obj.position.title if obj.position else (obj.role_title_applied or "General Application")
    get_target_role.short_description = "Target Role"

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank" style="color: #02AA69; font-weight: bold;">View File</a>', obj.resume.url)
        elif obj.resume_url:
            return format_html('<a href="{}" target="_blank" style="color: #3b82f6;">Link</a>', obj.resume_url)
        return "—"
    resume_link.short_description = "Resume"


@admin.register(ProductBuildInquiry)
class ProductBuildInquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company_name', 'project_type', 'budget_range', 'timeline', 'status', 'created_at']
    list_filter = ['project_type', 'budget_range', 'timeline', 'status', 'created_at']
    search_fields = ['full_name', 'company_name', 'work_email', 'phone', 'project_description']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(HireTalentInquiry)
class HireTalentInquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company_name', 'engagement_model', 'roles_needed', 'headcount', 'duration', 'status', 'created_at']
    list_filter = ['engagement_model', 'seniority_level', 'duration', 'status', 'created_at']
    search_fields = ['full_name', 'company_name', 'work_email', 'phone', 'roles_needed', 'technical_requirements']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(AcademyApplication)
class AcademyApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'track', 'experience_level', 'learning_mode', 'scholarship_requested', 'status', 'created_at']
    list_filter = ['track', 'experience_level', 'learning_mode', 'scholarship_requested', 'status', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'motivation_statement']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'source', 'resolved', 'created_at']
    list_filter = ['resolved', 'source', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    list_editable = ['resolved']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
