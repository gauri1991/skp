from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .storage import private_storage


def default_deliverable_expiry():
    from django.utils import timezone
    return timezone.now() + timedelta(days=90)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for portfolio cards")
    client = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name="projects")
    featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='portfolio/thumbnails/', blank=True)
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of technologies used")
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def primary_category(self):
        return self.categories.first()
    
    @property
    def get_technologies(self):
        """Return technologies as a list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='portfolio/images/')
    caption = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_thumbnail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.display_order}"

class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(help_text="Skill proficiency percentage (0-100)")
    category = models.CharField(max_length=50, choices=[
        ('technical', 'Technical'),
        ('software', 'Software'),
        ('professional', 'Professional'),
    ])
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'display_order']
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    responsibilities = models.JSONField(default=list, help_text="List of key responsibilities")
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        from datetime import date
        end = self.end_date or date.today()
        return end - self.start_date

class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-end_year']
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class ThemeSettings(models.Model):
    THEME_CHOICES = [
        ('professional', 'Professional Trust (Navy & Teal)'),
        ('minimal', 'Modern Minimal (Charcoal & Blue)'),
        ('warm', 'Warm Professional (Brown & Orange)'),
    ]
    
    theme_name = models.CharField(max_length=50, choices=THEME_CHOICES, default='professional')
    primary_color = models.CharField(max_length=7, default='#1e3a5f')
    secondary_color = models.CharField(max_length=7, default='#64748b')
    accent_color = models.CharField(max_length=7, default='#0891b2')
    background_color = models.CharField(max_length=7, default='#fafafa')
    surface_color = models.CharField(max_length=7, default='#ffffff')
    success_color = models.CharField(max_length=7, default='#10b981')
    warning_color = models.CharField(max_length=7, default='#f59e0b')
    error_color = models.CharField(max_length=7, default='#ef4444')
    info_color = models.CharField(max_length=7, default='#3b82f6')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Theme Settings"
        verbose_name_plural = "Theme Settings"
        
    def save(self, *args, **kwargs):
        # Ensure only one theme is active
        if self.is_active:
            ThemeSettings.objects.filter(is_active=True).update(is_active=False)
        
        # Set colors based on theme choice
        if self.theme_name == 'professional':
            self.primary_color = '#1e3a5f'
            self.secondary_color = '#64748b'
            self.accent_color = '#0891b2'
            self.background_color = '#fafafa'
            self.surface_color = '#ffffff'
        elif self.theme_name == 'minimal':
            self.primary_color = '#18181b'
            self.secondary_color = '#71717a'
            self.accent_color = '#2563eb'
            self.background_color = '#f4f4f5'
            self.surface_color = '#ffffff'
        elif self.theme_name == 'warm':
            self.primary_color = '#451a03'
            self.secondary_color = '#78716c'
            self.accent_color = '#ea580c'
            self.background_color = '#fef3c7'
            self.surface_color = '#ffffff'
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_theme_name_display()} - {'Active' if self.is_active else 'Inactive'}"
    
    @classmethod
    def get_active_theme(cls):
        theme = cls.objects.filter(is_active=True).first()
        if not theme:
            # Create default theme if none exists
            theme = cls.objects.create(theme_name='professional', is_active=True)
        return theme

class ProfessionalSummary(models.Model):
    content = models.TextField(help_text="Your professional summary")
    years_experience = models.PositiveIntegerField(default=0)
    specializations = models.TextField(blank=True, help_text="Comma-separated list of specializations")
    key_strengths = models.TextField(blank=True, help_text="Comma-separated list of key strengths")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Professional Summary"
        verbose_name_plural = "Professional Summaries"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            ProfessionalSummary.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Professional Summary - {'Active' if self.is_active else 'Inactive'}"
    
    @classmethod
    def get_active_summary(cls):
        return cls.objects.filter(is_active=True).first()

class ResumeExperience(models.Model):
    position_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    key_responsibilities = models.JSONField(default=list, help_text="List of key responsibilities")
    achievements = models.JSONField(default=list, blank=True, help_text="List of key achievements")
    technologies_used = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of technologies")
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', '-start_date']
        verbose_name = "Resume Experience"
    
    def __str__(self):
        return f"{self.position_title} at {self.company_name}"
    
    @property
    def date_range(self):
        start = self.start_date.strftime("%b %Y")
        end = "Present" if self.is_current else self.end_date.strftime("%b %Y") if self.end_date else ""
        return f"{start} - {end}"

class ResumeEducation(models.Model):
    degree_type = models.CharField(max_length=100, help_text="e.g., Master of Technology, Bachelor of Engineering")
    field_of_study = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    grade_type = models.CharField(max_length=50, choices=[
        ('cgpa', 'CGPA'),
        ('percentage', 'Percentage'),
        ('grade', 'Grade'),
        ('gpa', 'GPA'),
    ], default='cgpa')
    grade_value = models.CharField(max_length=50, blank=True, help_text="e.g., 9.30/10.0, 68%, First Class")
    thesis_title = models.CharField(max_length=500, blank=True)
    relevant_coursework = models.TextField(blank=True, help_text="Comma-separated list of relevant courses")
    honors_awards = models.TextField(blank=True, help_text="Comma-separated list of honors and awards")
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', '-end_year']
        verbose_name = "Resume Education"
    
    def __str__(self):
        return f"{self.degree_type} in {self.field_of_study} - {self.institution_name}"

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, help_text="Display name for the skill category")
    slug = models.SlugField(unique=True, help_text="URL-friendly identifier")
    icon = models.CharField(max_length=50, default='zap', help_text="Lucide icon name")
    description = models.TextField(blank=True, help_text="Optional description of this skill category")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which categories appear on resume")
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while SkillCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ResumeSkill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='intermediate')
    proficiency_percentage = models.PositiveIntegerField(default=50, help_text="Skill proficiency (0-100)")
    years_experience = models.PositiveIntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category__display_order', 'display_order', '-proficiency_percentage']
        verbose_name = "Resume Skill"
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    credential_id = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    is_lifetime = models.BooleanField(default=False)
    verification_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', '-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"
    
    @property
    def is_valid(self):
        if self.is_lifetime:
            return True
        if self.expiry_date:
            from datetime import date
            return self.expiry_date >= date.today()
        return True

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_achieved = models.DateField()
    category = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('professional', 'Professional'),
        ('project', 'Project'),
        ('award', 'Award'),
        ('publication', 'Publication'),
    ])
    organization = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', '-date_achieved']
    
    def __str__(self):
        return self.title


# Services System Models
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('civil', 'Civil Engineering'),
        ('environmental', 'Environmental Engineering'),
        ('design', 'Design & Planning'),
        ('construction', 'Construction Management'),
        ('consulting', 'Consulting Services'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='civil')
    short_description = models.CharField(max_length=300, help_text="Brief description for service cards")
    description = models.TextField(help_text="Detailed service description")
    icon = models.CharField(max_length=50, default='briefcase', help_text="Lucide icon name")
    image = models.ImageField(upload_to='services/icons/', blank=True, null=True, help_text="Custom service icon/image")
    features = models.JSONField(default=list, help_text="List of key features")
    process_steps = models.JSONField(default=list, help_text="Service delivery process steps")
    deliverables = models.JSONField(default=list, help_text="What clients receive")
    timeline = models.CharField(max_length=200, blank=True, help_text="Typical project duration")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    has_bom = models.BooleanField(default=False, help_text="Service includes Bill of Materials")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class ServiceTab(models.Model):
    TAB_TYPES = [
        ('info', 'Service Information'),
        ('requirements', 'Requirements'),
        ('quote', 'Get Quote'),
        ('bom', 'Bill of Materials'),
        ('portfolio', 'Portfolio'),
        ('process', 'Process'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tabs')
    tab_type = models.CharField(max_length=20, choices=TAB_TYPES)
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='info', help_text="Lucide icon name")
    content = models.TextField(blank=True, help_text="Tab content (for info/process tabs)")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
        unique_together = ['service', 'tab_type']
    
    def __str__(self):
        return f"{self.service.title} - {self.title}"


class ServiceRequirement(models.Model):
    FIELD_TYPES = [
        ('text', 'Text Input'),
        ('textarea', 'Text Area'),
        ('number', 'Number Input'),
        ('select', 'Select Dropdown'),
        ('checkbox', 'Checkbox'),
        ('file', 'File Upload'),
        ('date', 'Date Picker'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requirements')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    label = models.CharField(max_length=200)
    placeholder = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=300, blank=True)
    choices = models.JSONField(default=list, blank=True, help_text="For select fields: list of choices")
    is_required = models.BooleanField(default=False)
    affects_pricing = models.BooleanField(default=False)
    pricing_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
        unique_together = ['service', 'field_name']
    
    def __str__(self):
        return f"{self.service.title} - {self.label}"


class ServiceInquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Under Review'),
        ('quoted', 'Quote Sent'),
        ('accepted', 'Quote Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='inquiries')
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='service_inquiries',
        help_text="Linked client account, when the inquiry came from a logged-in client"
    )
    client_phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    project_title = models.CharField(max_length=300)
    requirements = models.JSONField(default=dict, help_text="Client requirements data")
    attachments = models.JSONField(default=list, help_text="List of uploaded file paths")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.service.title}"


class ServiceQuote(models.Model):
    inquiry = models.OneToOneField(ServiceInquiry, on_delete=models.CASCADE, related_name='quote')
    quote_number = models.CharField(max_length=50, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    validity_days = models.PositiveIntegerField(default=30)
    terms_conditions = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.quote_number:
            from datetime import datetime
            self.quote_number = f"QT-{datetime.now().strftime('%Y%m%d')}-{self.inquiry.id:04d}"
        
        # Calculate totals
        self.tax_amount = (self.subtotal * self.tax_rate) / 100
        self.total_amount = self.subtotal + self.tax_amount
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Quote {self.quote_number}"


class ServiceBOM(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bom_templates')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_template = models.BooleanField(default=True)
    inquiry = models.ForeignKey(ServiceInquiry, on_delete=models.CASCADE, null=True, blank=True, related_name='boms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.title} - {self.name}"
    
    @property
    def total_cost(self):
        return sum(item.total_cost for item in self.items.all())


class BOMItem(models.Model):
    UNIT_CHOICES = [
        ('nos', 'Numbers'),
        ('kg', 'Kilograms'),
        ('mt', 'Metric Tons'),
        ('sqm', 'Square Meters'),
        ('cum', 'Cubic Meters'),
        ('lm', 'Linear Meters'),
        ('hrs', 'Hours'),
        ('days', 'Days'),
        ('lot', 'Lot/Lump Sum'),
    ]
    
    bom = models.ForeignKey(ServiceBOM, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=100, default='Materials')
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    specification = models.CharField(max_length=300, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='nos')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'display_order', 'item_name']
    
    @property
    def total_cost(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"


# Client Portal Models
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    mobile = models.CharField(max_length=15, unique=True, help_text="Mobile number for login and OTP")
    company = models.CharField(max_length=200, blank=True, help_text="Company/Organization name")
    address = models.TextField(blank=True, help_text="Complete address")
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    
    # Verification status
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    # Preferences
    preferred_communication = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('both', 'Both Email and SMS'),
        ],
        default='both'
    )
    
    # AI access controls
    ai_enabled = models.BooleanField(default=True, help_text="Allow this client to use AI features")
    ai_daily_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Per-client daily AI generation limit override (blank = use each feature's default)"
    )

    # Account settings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.company or 'Individual'}"
    
    @property
    def full_address(self):
        """Return complete formatted address"""
        address_parts = [self.address, self.city, self.state, self.pincode, self.country]
        return ', '.join([part for part in address_parts if part])


class ClientOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('requested', 'Service Requested'),
        ('quoted', 'Quote Provided'),
        ('approved', 'Quote Approved'),
        ('in_progress', 'Work In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service_inquiry = models.OneToOneField(ServiceInquiry, on_delete=models.CASCADE, related_name='order')
    order_number = models.CharField(max_length=50, unique=True, help_text="Auto-generated order number")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='requested')
    
    # Pricing and payment
    quoted_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Timeline
    estimated_completion = models.DateField(null=True, blank=True)
    actual_completion = models.DateField(null=True, blank=True)
    
    # Internal notes (not visible to client)
    internal_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Order"
        verbose_name_plural = "Client Orders"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number like ORD-2024-001
            from datetime import datetime
            year = datetime.now().year
            count = ClientOrder.objects.filter(created_at__year=year).count() + 1
            self.order_number = f"ORD-{year}-{count:03d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order_number} - {self.service_inquiry.service.title}"
    
    @property
    def progress_percentage(self):
        """Calculate order progress percentage"""
        status_progress = {
            'requested': 10,
            'quoted': 20,
            'approved': 30,
            'in_progress': 60,
            'review': 85,
            'completed': 95,
            'delivered': 100,
            'cancelled': 0,
        }
        return status_progress.get(self.status, 0)
    
    @property
    def is_payment_due(self):
        """Check if payment is due"""
        if self.quoted_amount and self.paid_amount < self.quoted_amount:
            return True
        return False


class ClientDeliverable(models.Model):
    DELIVERABLE_STATUS_CHOICES = [
        ('preparing', 'Being Prepared'),
        ('ready', 'Ready for Download'),
        ('downloaded', 'Downloaded'),
        ('expired', 'Access Expired'),
    ]
    
    order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, related_name='deliverables')
    title = models.CharField(max_length=200, help_text="Title of the deliverable")
    description = models.TextField(blank=True, help_text="Description of the deliverable")
    file = models.FileField(storage=private_storage, upload_to='client_deliverables/', help_text="Private file storage (not URL-served)")
    file_type = models.CharField(max_length=50, blank=True, help_text="File type/category")
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    # Access control
    status = models.CharField(max_length=20, choices=DELIVERABLE_STATUS_CHOICES, default='preparing')
    access_token = models.CharField(max_length=100, unique=True, help_text="Secure access token")
    expires_at = models.DateTimeField(default=default_deliverable_expiry, help_text="When access expires")
    download_count = models.PositiveIntegerField(default=0)
    max_downloads = models.PositiveIntegerField(default=10, help_text="Maximum allowed downloads")
    
    # Tracking
    first_downloaded_at = models.DateTimeField(null=True, blank=True)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Deliverable"
        verbose_name_plural = "Client Deliverables"
    
    def save(self, *args, **kwargs):
        if not self.access_token:
            import uuid
            self.access_token = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.order.order_number}"
    
    @property
    def can_download(self):
        """Check if file can be downloaded"""
        from datetime import datetime
        from django.utils import timezone
        
        if self.status not in ('ready', 'downloaded'):
            return False
        if self.expires_at < timezone.now():
            return False
        if self.download_count >= self.max_downloads:
            return False
        return True
    
    @property
    def file_size_mb(self):
        """Return file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)


class ClientMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('inquiry', 'General Inquiry'),
        ('support', 'Support Ticket'),
        ('order_related', 'Order Related'),
        ('billing', 'Billing Question'),
        ('technical', 'Technical Issue'),
    ]
    
    MESSAGE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_client', 'Waiting for Client Response'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    
    # Message details
    subject = models.CharField(max_length=200)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='inquiry')
    content = models.TextField()
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS_CHOICES, default='open')
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='medium'
    )
    
    # Admin response
    admin_response = models.TextField(blank=True)
    admin_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='handled_messages'
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # File attachments
    attachment = models.FileField(upload_to='client_messages/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Message"
        verbose_name_plural = "Client Messages"
    
    def __str__(self):
        return f"{self.client.get_full_name() or self.client.username} - {self.subject}"


class ClientNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('order_update', 'Order Status Update'),
        ('delivery_ready', 'Deliverable Ready'),
        ('payment_due', 'Payment Due'),
        ('system', 'System Notification'),
        ('promotional', 'Promotional'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    
    # Status
    is_read = models.BooleanField(default=False)
    sent_via_email = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    
    # Related objects
    order = models.ForeignKey(ClientOrder, on_delete=models.CASCADE, null=True, blank=True)
    deliverable = models.ForeignKey(ClientDeliverable, on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Notification"
        verbose_name_plural = "Client Notifications"
    
    def __str__(self):
        return f"{self.client.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


# Homepage Content Management
class HomepageSection(models.Model):
    """
    Model to manage homepage sections
    """
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('about', 'About Section'),
        ('services', 'Services Preview'),
        ('portfolio', 'Portfolio Showcase'),
        ('testimonials', 'Testimonials'),
        ('contact', 'Contact Section'),
        ('stats', 'Statistics Section'),
        ('skills', 'Skills Section'),
    ]
    
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    title = models.CharField(max_length=200)
    is_enabled = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'section_type']
        verbose_name = "Homepage Section"
        verbose_name_plural = "Homepage Sections"
    
    def __str__(self):
        return f"{self.get_section_type_display()} - {'Enabled' if self.is_enabled else 'Disabled'}"


class HomepageContent(models.Model):
    """
    Model to store content for homepage sections
    """
    section = models.OneToOneField(HomepageSection, on_delete=models.CASCADE, related_name='content')
    
    # Hero Section Fields
    hero_title = models.CharField(max_length=200, blank=True, help_text="Main headline for hero section")
    hero_subtitle = models.CharField(max_length=300, blank=True, help_text="Subtitle for hero section")
    hero_description = models.TextField(blank=True, help_text="Hero description text")
    hero_image = models.ImageField(upload_to='homepage/hero/', blank=True, null=True)
    hero_cta_primary_text = models.CharField(max_length=50, blank=True, default="View Portfolio")
    hero_cta_primary_url = models.CharField(max_length=200, blank=True, default="/portfolio/")
    hero_cta_secondary_text = models.CharField(max_length=50, blank=True, default="Contact Me")
    hero_cta_secondary_url = models.CharField(max_length=200, blank=True, default="/contact/")
    
    # Hero Stats Fields
    hero_stat1_number = models.CharField(max_length=10, blank=True, default="50+", help_text="First stat number")
    hero_stat1_label = models.CharField(max_length=50, blank=True, default="Projects Completed", help_text="First stat label")
    hero_stat2_number = models.CharField(max_length=10, blank=True, default="5+", help_text="Second stat number")
    hero_stat2_label = models.CharField(max_length=50, blank=True, default="Years Experience", help_text="Second stat label")
    hero_stat3_number = models.CharField(max_length=10, blank=True, default="30+", help_text="Third stat number")
    hero_stat3_label = models.CharField(max_length=50, blank=True, default="Patent Illustrations", help_text="Third stat label")
    hero_stat4_number = models.CharField(max_length=10, blank=True, default="100%", help_text="Fourth stat number")
    hero_stat4_label = models.CharField(max_length=50, blank=True, default="Client Satisfaction", help_text="Fourth stat label")
    
    # About Section Fields
    about_title = models.CharField(max_length=200, blank=True, default="About Me")
    about_description = models.TextField(blank=True, help_text="About section description")
    about_image = models.ImageField(upload_to='homepage/about/', blank=True, null=True)
    about_years_experience = models.IntegerField(blank=True, null=True)
    about_projects_completed = models.IntegerField(blank=True, null=True)
    about_clients_served = models.IntegerField(blank=True, null=True)
    
    # About Key Points (checkmark items)
    about_point1 = models.CharField(max_length=100, blank=True, default="Professional Engineering Design", help_text="First key point")
    about_point2 = models.CharField(max_length=100, blank=True, default="Technical Patent Illustrations", help_text="Second key point")
    about_point3 = models.CharField(max_length=100, blank=True, default="Environmental Engineering Solutions", help_text="Third key point") 
    about_point4 = models.CharField(max_length=100, blank=True, default="Sustainable Development Practices", help_text="Fourth key point")
    
    # About Quick Facts
    about_fact1_label = models.CharField(max_length=50, blank=True, default="Experience", help_text="First fact label")
    about_fact1_value = models.CharField(max_length=50, blank=True, default="5+ Years", help_text="First fact value")
    about_fact2_label = models.CharField(max_length=50, blank=True, default="Projects Completed", help_text="Second fact label")
    about_fact2_value = models.CharField(max_length=50, blank=True, default="50+", help_text="Second fact value")
    about_fact3_label = models.CharField(max_length=50, blank=True, default="Specialization", help_text="Third fact label")
    about_fact3_value = models.CharField(max_length=50, blank=True, default="Civil Engineering", help_text="Third fact value")
    about_fact4_label = models.CharField(max_length=50, blank=True, default="Location", help_text="Fourth fact label")
    about_fact4_value = models.CharField(max_length=50, blank=True, default="India", help_text="Fourth fact value")
    
    # Services Section Fields
    services_title = models.CharField(max_length=200, blank=True, default="My Services")
    services_subtitle = models.CharField(max_length=300, blank=True)
    services_description = models.TextField(blank=True)
    featured_services = models.ManyToManyField(Service, blank=True, help_text="Select services to feature on homepage")
    
    # Portfolio Section Fields
    portfolio_title = models.CharField(max_length=200, blank=True, default="My Work")
    portfolio_subtitle = models.CharField(max_length=300, blank=True)
    portfolio_description = models.TextField(blank=True)
    featured_projects = models.ManyToManyField(Project, blank=True, help_text="Select projects to feature on homepage")
    
    # Testimonials Section Fields
    testimonials_title = models.CharField(max_length=200, blank=True, default="What Clients Say")
    testimonials_subtitle = models.CharField(max_length=300, blank=True)
    testimonials_description = models.TextField(blank=True)
    featured_testimonials = models.ManyToManyField(Testimonial, blank=True, help_text="Select testimonials to feature on homepage")
    
    # Testimonials Display Options
    TESTIMONIALS_DISPLAY_CHOICES = [
        ('grid', 'Static Grid (3 columns)'),
        ('slider', 'Slider with Navigation'),
        ('continuous', 'Continuous Horizontal Scroll'),
    ]
    testimonials_display_mode = models.CharField(
        max_length=20, 
        choices=TESTIMONIALS_DISPLAY_CHOICES, 
        default='grid',
        help_text="Choose how testimonials are displayed on the homepage"
    )
    
    # Contact Section Fields
    contact_title = models.CharField(max_length=200, blank=True, default="Ready to Start Your Project?")
    contact_subtitle = models.CharField(max_length=300, blank=True)
    contact_description = models.TextField(blank=True, default="Let's work together to bring your engineering vision to life with professional expertise and innovative solutions.")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    contact_linkedin_url = models.URLField(blank=True)
    contact_facebook_url = models.URLField(blank=True)
    contact_twitter_url = models.URLField(blank=True)
    contact_instagram_url = models.URLField(blank=True)
    
    # Contact/CTA Button Fields
    contact_cta_primary_text = models.CharField(max_length=50, blank=True, default="Contact Me Today", help_text="Primary CTA button text")
    contact_cta_primary_url = models.CharField(max_length=200, blank=True, default="/contact", help_text="Primary CTA button URL")
    contact_cta_secondary_text = models.CharField(max_length=50, blank=True, default="View My Work", help_text="Secondary CTA button text")
    contact_cta_secondary_url = models.CharField(max_length=200, blank=True, default="/portfolio", help_text="Secondary CTA button URL")
    
    # Stats Section Fields
    stats_title = models.CharField(max_length=200, blank=True, default="By The Numbers")
    stats_subtitle = models.CharField(max_length=300, blank=True)
    
    # Skills Section Fields
    skills_title = models.CharField(max_length=200, blank=True, default="Skills & Expertise")
    skills_subtitle = models.CharField(max_length=300, blank=True)
    skills_description = models.TextField(blank=True)
    featured_skills = models.ManyToManyField(Skill, blank=True, help_text="Select skills to feature on homepage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Contents"
    
    def __str__(self):
        return f"Content for {self.section.get_section_type_display()}"


class SiteSettings(models.Model):
    """
    Singleton model to store site-wide settings like header, footer, meta tags etc.
    """
    # Meta Tags & SEO
    site_title = models.CharField(max_length=100, default="Sumithra KP - Civil Engineer & Patent Illustrator", 
                                help_text="Main site title for browser tab")
    meta_description = models.TextField(max_length=300, 
                                      default="Professional Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.",
                                      help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=200, 
                                   default="civil engineering, patent illustrations, environmental engineering, sumithra kp",
                                   help_text="SEO keywords (comma-separated)")
    og_url = models.URLField(default="https://sumithrakp.com", help_text="Open Graph URL")
    
    # Header/Logo
    logo_alt_text = models.CharField(max_length=50, default="Sumithra KP", help_text="Logo alt text")
    logo_fallback_text = models.CharField(max_length=50, default="Sumithra KP", help_text="Text shown if logo fails to load")
    
    # Footer Company Info
    footer_company_name = models.CharField(max_length=50, default="Sumithra KP", help_text="Company name in footer")
    footer_description = models.TextField(max_length=200, 
                                        default="Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.",
                                        help_text="Company description in footer")
    footer_copyright_year = models.IntegerField(default=2024, help_text="Copyright year")
    footer_copyright_text = models.CharField(max_length=100, default="All rights reserved.", 
                                           help_text="Copyright text after year")
    
    # Social Media Links
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    email_address = models.EmailField(blank=True, help_text="Contact email address")  
    phone_number = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    
    # Footer Services List
    footer_service1 = models.CharField(max_length=50, default="Civil Engineering Design", help_text="First footer service")
    footer_service2 = models.CharField(max_length=50, default="Patent Illustrations", help_text="Second footer service")  
    footer_service3 = models.CharField(max_length=50, default="Environmental Engineering", help_text="Third footer service")
    
    # Contact Information
    business_address = models.TextField(blank=True, help_text="Business address for footer")
    business_phone = models.CharField(max_length=20, blank=True, help_text="Business phone number")
    business_email = models.EmailField(blank=True, help_text="Business email address")
    
    # Contact Page Content
    contact_page_title = models.CharField(max_length=100, default="Contact Me", help_text="Contact page main title")
    contact_page_subtitle = models.TextField(default="Let's discuss your project and how I can help bring your vision to life with professional engineering expertise.", help_text="Contact page subtitle/description")
    
    # Contact Form Section
    contact_form_title = models.CharField(max_length=50, default="Send a Message", help_text="Contact form section title")
    contact_success_message = models.CharField(max_length=200, default="Thank you! Your message has been sent successfully.", help_text="Form success message")
    contact_success_note = models.CharField(max_length=200, default="I typically respond within 24-48 hours.", help_text="Additional note after success message")
    
    # Contact Information Section
    contact_info_title = models.CharField(max_length=50, default="Get in Touch", help_text="Contact info section title")
    contact_primary_email = models.EmailField(default="contact@sumithrakp.com", help_text="Primary contact email")
    contact_primary_phone = models.CharField(max_length=20, default="+91 829 624 4110", help_text="Primary contact phone")
    contact_location = models.CharField(max_length=100, default="Mysore, Karnataka, India", help_text="Business location")
    contact_company = models.CharField(max_length=100, default="Sigvitas & Company", help_text="Current company/employment")
    contact_response_time = models.CharField(max_length=200, default="I typically respond to inquiries within 24-48 hours.", help_text="Response time description")
    
    # Services & Availability Section
    services_availability_title = models.CharField(max_length=50, default="Services & Availability", help_text="Services section title")
    services_availability_subtitle = models.CharField(max_length=200, default="Professional consulting services with flexible scheduling", help_text="Services section subtitle")
    
    # Professional Services
    professional_services_title = models.CharField(max_length=50, default="Professional Services", help_text="Professional services section title")
    service_item_1 = models.CharField(max_length=100, default="Civil Engineering Consultation", help_text="First service item")
    service_item_2 = models.CharField(max_length=100, default="AERMOD Modeling and Environmental Analysis", help_text="Second service item")
    service_item_3 = models.CharField(max_length=100, default="Building Design and Layout Planning", help_text="Third service item")
    service_item_4 = models.CharField(max_length=100, default="Patent Illustrations and Technical Drawings", help_text="Fourth service item")
    service_item_5 = models.CharField(max_length=100, default="Construction Project Management", help_text="Fifth service item")
    
    # Availability Section
    availability_title = models.CharField(max_length=50, default="Current Availability", help_text="Availability section title")
    availability_description = models.TextField(default="I am currently available for select consulting projects that can be done alongside my full-time position.", help_text="Availability description")
    availability_note = models.CharField(max_length=200, default="Please contact me with project details to discuss availability and timelines.", help_text="Availability note")
    
    # Response Time Section
    response_time_title = models.CharField(max_length=50, default="Response Time", help_text="Response time section title")
    response_time_hours = models.CharField(max_length=10, default="24-48", help_text="Response time in hours")
    response_time_description = models.CharField(max_length=200, default="I typically respond to all inquiries within 24-48 hours.", help_text="Response time description")
    
    # Response Time Features
    response_feature_1 = models.CharField(max_length=100, default="Quick response within 24-48 hours", help_text="First response feature")
    response_feature_2 = models.CharField(max_length=100, default="Professional consultation guaranteed", help_text="Second response feature")
    response_feature_3 = models.CharField(max_length=100, default="Detailed project analysis provided", help_text="Third response feature")
    response_feature_4 = models.CharField(max_length=100, default="Free initial consultation call", help_text="Fourth response feature")
    response_feature_5 = models.CharField(max_length=100, default="Transparent pricing and timelines", help_text="Fifth response feature")
    
    # FAQ Section
    faq_title = models.CharField(max_length=50, default="Frequently Asked Questions", help_text="FAQ section title")
    faq_subtitle = models.CharField(max_length=200, default="Common questions about my services and process", help_text="FAQ section subtitle")
    
    faq_question_1 = models.CharField(max_length=200, default="What types of projects do you work on?", help_text="First FAQ question")
    faq_answer_1 = models.TextField(default="I specialize in civil engineering design, patent illustrations, environmental engineering solutions, residential and commercial building design, infrastructure planning, and technical documentation for patent applications.", help_text="First FAQ answer")
    
    faq_question_2 = models.CharField(max_length=200, default="What is your typical project timeline?", help_text="Second FAQ question")
    faq_answer_2 = models.TextField(default="Project timelines vary based on scope and complexity. Simple patent illustrations may take 1-2 weeks, while comprehensive building designs can take 4-8 weeks. I provide detailed timelines during initial consultation.", help_text="Second FAQ answer")
    
    faq_question_3 = models.CharField(max_length=200, default="Do you provide ongoing support after project completion?", help_text="Third FAQ question")
    faq_answer_3 = models.TextField(default="Yes, I provide ongoing support to ensure successful project implementation. This includes answering questions, minor revisions, and assistance with regulatory submissions when needed.", help_text="Third FAQ answer")
    
    faq_question_4 = models.CharField(max_length=200, default="What software and tools do you use?", help_text="Fourth FAQ question")
    faq_answer_4 = models.TextField(default="I use industry-standard software including AutoCAD, MS Visio, Civil 3D, GIS software, remote sensing tools, and AERMOD for environmental modeling. All deliverables are provided in standard formats.", help_text="Fourth FAQ answer")
    
    # Call to Action Section
    cta_title = models.CharField(max_length=100, default="Ready to Get Started?", help_text="Call to action section title")
    cta_description = models.TextField(default="Let's discuss your project requirements and explore how I can help achieve your engineering goals.", help_text="Call to action description")
    cta_email_button_text = models.CharField(max_length=50, default="Email Me", help_text="Email button text")
    cta_phone_button_text = models.CharField(max_length=50, default="Call Now", help_text="Phone button text")
    
    # Quick Links Section
    quick_link_1_text = models.CharField(max_length=50, blank=True, help_text="First quick link text (optional)")
    quick_link_1_url = models.CharField(max_length=100, blank=True, help_text="First quick link URL (optional)")
    quick_link_2_text = models.CharField(max_length=50, blank=True, help_text="Second quick link text (optional)") 
    quick_link_2_url = models.CharField(max_length=100, blank=True, help_text="Second quick link URL (optional)")
    quick_link_3_text = models.CharField(max_length=50, blank=True, help_text="Third quick link text (optional)")
    quick_link_3_url = models.CharField(max_length=100, blank=True, help_text="Third quick link URL (optional)")
    quick_link_4_text = models.CharField(max_length=50, blank=True, help_text="Fourth quick link text (optional)")
    quick_link_4_url = models.CharField(max_length=100, blank=True, help_text="Fourth quick link URL (optional)")
    quick_link_5_text = models.CharField(max_length=50, blank=True, help_text="Fifth quick link text (optional)")
    quick_link_5_url = models.CharField(max_length=100, blank=True, help_text="Fifth quick link URL (optional)")
    quick_link_6_text = models.CharField(max_length=50, blank=True, help_text="Sixth quick link text (optional)")
    quick_link_6_url = models.CharField(max_length=100, blank=True, help_text="Sixth quick link URL (optional)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and SiteSettings.objects.exists():
            # If trying to create a new instance but one already exists,
            # update the existing one instead
            existing = SiteSettings.objects.first()
            existing.site_title = self.site_title
            existing.meta_description = self.meta_description
            existing.meta_keywords = self.meta_keywords
            existing.og_url = self.og_url
            existing.logo_alt_text = self.logo_alt_text
            existing.logo_fallback_text = self.logo_fallback_text
            existing.footer_company_name = self.footer_company_name
            existing.footer_description = self.footer_description
            existing.footer_copyright_year = self.footer_copyright_year
            existing.footer_copyright_text = self.footer_copyright_text
            existing.linkedin_url = self.linkedin_url
            existing.email_address = self.email_address
            existing.phone_number = self.phone_number
            existing.twitter_url = self.twitter_url
            existing.instagram_url = self.instagram_url
            existing.footer_service1 = self.footer_service1
            existing.footer_service2 = self.footer_service2
            existing.footer_service3 = self.footer_service3
            existing.business_address = self.business_address
            existing.business_phone = self.business_phone
            existing.business_email = self.business_email
            existing.save()
            return existing
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the site settings instance, create one if it doesn't exist"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_title': 'Sumithra KP - Civil Engineer & Patent Illustrator',
                'meta_description': 'Professional Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.',
            }
        )
        return settings
    
    def __str__(self):
        return "Site Settings"


class ClientLogo(models.Model):
    """Model to store client/partner logos for the 'Trusted By' section"""
    name = models.CharField(max_length=200, help_text="Client/Company name")
    logo = models.ImageField(upload_to='clients/', help_text="Client logo image")
    website = models.URLField(blank=True, help_text="Client website URL (optional)")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which logos appear")
    is_active = models.BooleanField(default=True, help_text="Show this logo on the website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Client Logo"
        verbose_name_plural = "Client Logos"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100, help_text="Full name of the person")
    email = models.EmailField(help_text="Email address")
    subject = models.CharField(max_length=200, help_text="Subject of the message")
    message = models.TextField(help_text="Message content")
    
    # Additional fields
    phone = models.CharField(max_length=20, blank=True, help_text="Optional phone number")
    company = models.CharField(max_length=100, blank=True, help_text="Optional company name")
    
    # System fields
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP address of the sender")
    user_agent = models.TextField(blank=True, help_text="Browser user agent")
    
    # Status fields
    is_read = models.BooleanField(default=False, help_text="Whether the message has been read")
    is_replied = models.BooleanField(default=False, help_text="Whether the message has been replied to")
    reply_notes = models.TextField(blank=True, help_text="Internal notes for replies")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def mark_as_read(self):
        """Mark the message as read"""
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])
    
    def mark_as_replied(self, notes=""):
        """Mark the message as replied with optional notes"""
        self.is_replied = True
        if notes:
            self.reply_notes = notes
        self.save(update_fields=['is_replied', 'reply_notes', 'updated_at'])


# ============ AI Platform (Phase 3) ============

class AIProvider(models.Model):
    """A configured AI provider (LLM / image / video API). Keys live here so the
    dashboard can manage everything without code deploys."""
    ADAPTER_CHOICES = [
        ('anthropic', 'Anthropic (Claude)'),
        ('openai_compatible', 'OpenAI-compatible (generic)'),
        ('gemini', 'Google Gemini'),
        ('deepseek', 'DeepSeek'),
        ('seedance', 'Seedance (video)'),
        ('wan', 'WAN / Alibaba (video)'),
        ('higgsfield', 'Higgsfield (video)'),
    ]
    KIND_CHOICES = [
        ('text', 'Text'), ('image', 'Image'), ('video', 'Video'),
        ('multimodal', 'Multimodal'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    adapter_type = models.CharField(max_length=30, choices=ADAPTER_CHOICES)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='text')
    api_key = models.CharField(max_length=255, blank=True)
    base_url = models.URLField(blank=True, help_text="Override the adapter's default endpoint")
    default_model = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    extra_config = models.JSONField(default=dict, blank=True,
        help_text="Adapter knobs: max_tokens, timeout, submit_path/poll_path for video, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'AI Provider'

    def __str__(self):
        return f"{self.name} ({self.default_model})"

    @property
    def masked_key(self):
        if not self.api_key:
            return '(not set)'
        return f"••••{self.api_key[-4:]}"


class ServiceAIFeature(models.Model):
    """A client-facing AI tool attached to a service, fully prompt-configurable."""
    FEATURE_TYPE_CHOICES = [('text', 'Text'), ('image', 'Image'), ('video', 'Video')]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ai_features')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(help_text="Client-facing explanation of what this tool does")
    feature_type = models.CharField(max_length=10, choices=FEATURE_TYPE_CHOICES, default='text')
    provider = models.ForeignKey(AIProvider, on_delete=models.PROTECT, related_name='features')
    model_override = models.CharField(max_length=100, blank=True)
    system_prompt = models.TextField()
    user_prompt_template = models.TextField(
        help_text="Use {field_name} placeholders matching input field names")
    input_fields = models.JSONField(default=list,
        help_text='[{"name","label","type","required","choices","help"}] - type: text/textarea/select/number/file')
    output_guidance = models.TextField(blank=True,
        help_text="Appended to the system prompt (formatting rules)")
    allow_file_upload = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    daily_limit_per_client = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']
        unique_together = ['service', 'slug']
        verbose_name = 'Service AI Feature'

    def __str__(self):
        return f"{self.service.title} - {self.title}"

    @property
    def effective_model(self):
        return self.model_override or self.provider.default_model


class AIGeneration(models.Model):
    """One AI run by a client. Text/image complete synchronously; video is queued
    and completed by the process_ai_jobs cron worker."""
    STATUS_CHOICES = [
        ('queued', 'Queued'), ('running', 'Running'),
        ('succeeded', 'Succeeded'), ('failed', 'Failed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_generations')
    feature = models.ForeignKey(ServiceAIFeature, on_delete=models.SET_NULL, null=True,
                                related_name='generations')
    # Snapshots survive feature/provider deletion
    feature_title = models.CharField(max_length=200, blank=True)
    provider_name = models.CharField(max_length=100, blank=True)
    model_used = models.CharField(max_length=100, blank=True)
    order = models.ForeignKey(ClientOrder, on_delete=models.SET_NULL, null=True, blank=True)
    inputs = models.JSONField(default=dict)
    input_file = models.FileField(storage=private_storage, upload_to='ai_inputs/%Y/%m/',
                                  null=True, blank=True)
    rendered_prompt = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='queued', db_index=True)
    output_text = models.TextField(blank=True)
    output_file = models.FileField(storage=private_storage, upload_to='ai_outputs/%Y/%m/',
                                   null=True, blank=True)
    output_mime = models.CharField(max_length=50, blank=True)
    provider_job_id = models.CharField(max_length=200, blank=True)
    tokens_input = models.PositiveIntegerField(null=True, blank=True)
    tokens_output = models.PositiveIntegerField(null=True, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['client', 'created_at'])]
        verbose_name = 'AI Generation'

    def __str__(self):
        return f"{self.feature_title or 'AI'} for {self.client} ({self.status})"

    @classmethod
    def used_today(cls, client, feature):
        from django.utils import timezone
        return cls.objects.filter(
            client=client, feature=feature,
            created_at__date=timezone.localdate()
        ).exclude(status='failed').count()
