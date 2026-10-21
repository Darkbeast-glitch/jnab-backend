from django.db import models
from django.utils.text import slugify


class JobPosition(models.Model):
    """
    Job and Career openings at JNAB Innovations, populated and managed via Django backend/admin.
    """
    DEPARTMENT_CHOICES = [
        ('engineering', 'Software Engineering'),
        ('design', 'Product & UI/UX Design'),
        ('talent', 'Academy & Technical Education'),
        ('operations', 'Operations & Growth'),
    ]

    WORK_TYPE_CHOICES = [
        ('remote', '100% Remote'),
        ('hybrid', 'Accra Tech Hub / Hybrid'),
        ('onsite', 'On-Site (Accra, Ghana)'),
    ]

    EMPLOYMENT_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract / Project Pod'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='engineering')
    location = models.CharField(max_length=150, default="Accra, Ghana · Global Remote")
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES, default='remote')
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=100, default="Senior (3+ yrs)")
    salary_range = models.CharField(max_length=100, blank=True, default="Competitive + Equity")
    
    summary = models.TextField(help_text="Short teaser shown on career card in the frontend")
    description = models.TextField(help_text="Full role narrative and scope")
    responsibilities = models.TextField(help_text="Bullet points or markdown of key deliverables")
    requirements = models.TextField(help_text="Must-have qualifications, technical stack, and experience")
    benefits = models.TextField(blank=True, help_text="Equipment, health coverage, learning stipend, flex hours")
    
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this job from the website")
    featured = models.BooleanField(default=False, help_text="Highlight role with a featured badge")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = "Career Opening"
        verbose_name_plural = "Career Openings"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while JobPosition.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_department_display()})"


class JobApplication(models.Model):
    """
    Dedicated application form for engineering, design, and operations candidates.
    Distinct from client product inquiries.
    """
    STATUS_CHOICES = [
        ('new', 'New Applicant'),
        ('reviewing', 'In Portfolio Review'),
        ('interview', 'Interview Scheduled'),
        ('offer', 'Offer Extended'),
        ('rejected', 'Not Moving Forward'),
    ]

    position = models.ForeignKey(
        JobPosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
        help_text="Leave blank if this is a general proactive talent application"
    )
    role_title_applied = models.CharField(max_length=200, blank=True, help_text="Target role if not selecting a specific opening")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    location = models.CharField(max_length=150, blank=True, help_text="City, Country")
    years_of_experience = models.CharField(max_length=50, blank=True, help_text="e.g. 4 years")
    
    portfolio_url = models.URLField(blank=True, help_text="Figma, Personal Website, Behance")
    github_url = models.URLField(blank=True, help_text="GitHub or GitLab profile")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    
    resume = models.FileField(upload_to="resumes/%Y/%m/", blank=True, null=True, help_text="PDF or DOCX resume upload")
    resume_url = models.URLField(blank=True, help_text="Alternative Drive/Notion/Dropbox link if not uploading file")
    cover_note = models.TextField(help_text="Why JNAB? Tell us about the most impactful system or design you've engineered.")
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text="Internal hiring team notes & interview feedback")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"

    def __str__(self):
        target = self.position.title if self.position else (self.role_title_applied or "General Talent")
        return f"{self.full_name} → {target}"


class ProductBuildInquiry(models.Model):
    """
    Dedicated form for ventures and scale-ups requesting end-to-end product design and software development.
    """
    PROJECT_TYPE_CHOICES = [
        ('full_cycle', 'End-to-End Product Build (Design + Web + Mobile + Cloud)'),
        ('mobile_app', 'Mobile Application (iOS & Android)'),
        ('web_platform', 'Web Platform / SaaS Application'),
        ('enterprise_system', 'Enterprise Backend & Distributed Architecture'),
        ('ui_ux_design', 'Digital Product Design & Design Systems'),
        ('cloud_devops', 'Cloud Infrastructure & DevOps Automation'),
    ]

    BUDGET_CHOICES = [
        ('tier_1', '$5,000 – $15,000'),
        ('tier_2', '$15,000 – $30,000'),
        ('tier_3', '$30,000 – $60,000'),
        ('tier_4', '$60,000+ (Enterprise Scope)'),
        ('undecided', 'To Be Defined During Discovery'),
    ]

    TIMELINE_CHOICES = [
        ('immediate', 'Immediate Launch (< 1 month)'),
        ('standard', '1 – 3 Months (Standard MVP)'),
        ('medium', '3 – 6 Months (Complete Scale)'),
        ('flexible', 'Flexible / Strategy Exploration'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted / Discovery Call'),
        ('proposal', 'Proposal & Architecture Spec Sent'),
        ('won', 'Contract Signed (Won)'),
        ('lost', 'Closed (Lost)'),
    ]

    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    work_email = models.EmailField()
    phone = models.CharField(max_length=50)
    
    project_type = models.CharField(max_length=60, choices=PROJECT_TYPE_CHOICES, default='full_cycle')
    target_platforms = models.CharField(max_length=250, blank=True, help_text="e.g. iOS, Android, Web, REST API")
    budget_range = models.CharField(max_length=50, choices=BUDGET_CHOICES, default='tier_2')
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, default='standard')
    
    project_description = models.TextField(help_text="Problem statement, core features, target users, and desired deliverables")
    existing_spec_url = models.URLField(blank=True, help_text="Link to Figma, PRD, Notion document, or RFP")
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    internal_notes = models.TextField(blank=True, help_text="Internal notes for proposal and estimation")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Build Inquiry"
        verbose_name_plural = "Product Build Inquiries"

    def __str__(self):
        comp = f" ({self.company_name})" if self.company_name else ""
        return f"{self.full_name}{comp} — {self.get_project_type_display()}"


class HireTalentInquiry(models.Model):
    """
    Dedicated form for companies wanting to embed senior African developers or deploy an autonomous tech pod.
    """
    ENGAGEMENT_CHOICES = [
        ('embedded_talent', 'Embedded Senior Engineers (Integrated with your team)'),
        ('dedicated_pod', 'Autonomous Tech Pod (Full squad: Frontend, Backend, QA, PM)'),
        ('staff_augmentation', 'Targeted Staff Augmentation (Short/Medium term)'),
        ('tech_advisory', 'Fractional CTO & Architecture Advisory'),
    ]

    SENIORITY_CHOICES = [
        ('mid', 'Mid-Level (2–4 yrs experience)'),
        ('senior', 'Senior (4–7+ yrs experience)'),
        ('lead', 'Principal / Engineering Lead'),
        ('mixed', 'Mixed Seniority Squad'),
    ]

    DURATION_CHOICES = [
        ('3_months', '3 Months (Sprint)'),
        ('6_months', '6 Months'),
        ('12_months_plus', '12+ Months (Long-Term Strategic Partner)'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Request'),
        ('matching', 'Vetting & Matching Talent'),
        ('interviewing', 'Client Interviews Underway'),
        ('deployed', 'Engineers Deployed'),
        ('closed', 'Closed'),
    ]

    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    work_email = models.EmailField()
    phone = models.CharField(max_length=50)
    
    engagement_model = models.CharField(max_length=50, choices=ENGAGEMENT_CHOICES, default='embedded_talent')
    roles_needed = models.CharField(max_length=300, help_text="e.g. 2x React / TypeScript Devs, 1x Python Backend, 1x UI/UX Designer")
    seniority_level = models.CharField(max_length=50, choices=SENIORITY_CHOICES, default='senior')
    headcount = models.CharField(max_length=50, default="1–2 Engineers")
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES, default='6_months')
    start_date = models.CharField(max_length=100, default="Within 2 Weeks")
    timezone_overlap = models.CharField(max_length=150, default="GMT / European / US Eastern overlap (min 4 hours)")
    
    technical_requirements = models.TextField(help_text="Key stack, tools, workflows (e.g., Docker, AWS, React, Django, Jest, Agile)")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Hire Talent Inquiry"
        verbose_name_plural = "Hire Talent Inquiries"

    def __str__(self):
        return f"{self.full_name} ({self.company_name}) — {self.get_engagement_model_display()}"


class AcademyApplication(models.Model):
    """
    Dedicated application form for JNAB Academy technical fellowships and enterprise upskilling.
    """
    TRACK_CHOICES = [
        ('product_design', 'Track 01: Product Design & Systems Architecture'),
        ('full_stack', 'Track 02: Full-Stack Application Engineering (Web & Mobile)'),
        ('enterprise_upskilling', 'Track 03: Enterprise Team Technical Upskilling'),
    ]

    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (Strong aptitude, foundational basics)'),
        ('intermediate', 'Intermediate (1–2 yrs coding/design experience)'),
        ('advanced', 'Advanced Practitioner seeking senior mastery'),
    ]

    LEARNING_MODE_CHOICES = [
        ('bootcamp', 'Full-Time Intensive Fellowship Cohort'),
        ('part_time', 'Part-Time / Evening & Weekend Track'),
        ('corporate', 'Corporate / Company Sponsored Training'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Application Submitted'),
        ('assessment_sent', 'Technical Assessment Sent'),
        ('interviewing', 'Admissions Interview'),
        ('accepted', 'Accepted into Cohort'),
        ('waitlisted', 'Waitlisted'),
        ('enrolled', 'Enrolled & Active'),
        ('rejected', 'Declined'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    
    track = models.CharField(max_length=50, choices=TRACK_CHOICES, default='full_stack')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='intermediate')
    learning_mode = models.CharField(max_length=50, choices=LEARNING_MODE_CHOICES, default='bootcamp')
    
    portfolio_or_github = models.URLField(blank=True, help_text="GitHub profile, portfolio link, or code samples")
    motivation_statement = models.TextField(help_text="What do you aspire to build, and how will JNAB Academy accelerate your technical career?")
    scholarship_requested = models.BooleanField(default=False, help_text="Check if applying for need-based tuition subsidy")
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')
    reviewer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Academy Application"
        verbose_name_plural = "Academy Applications"

    def __str__(self):
        return f"{self.full_name} — {self.get_track_display()}"


class ContactInquiry(models.Model):
    """
    General consultation, quick quote trigger, or general question from the website CTA or footer.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=250, default="Project Inquiry")
    message = models.TextField()
    source = models.CharField(max_length=100, default="Website CTA", help_text="Where on the site this was triggered")
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "General Contact Inquiry"
        verbose_name_plural = "General Contact Inquiries"

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
