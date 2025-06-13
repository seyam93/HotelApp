from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    hotels = models.ManyToManyField('hotels.Hotel', related_name='faqs')

    def __str__(self):
        return self.question
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['question']

# Partner model
class Partner(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='partners')
    partner_name = models.CharField(max_length=255)
    partner_description = models.TextField(null=True,blank=True)
    partner_image = models.ImageField(upload_to='partners', null=True,blank=True)
    partner_url = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.partner_name
    
    class Meta:
        verbose_name = "Partnership Corporates"
        
# Contact Message Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='contact_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
# This model is used to store contact form submissions.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    hotel = models.ForeignKey('hotels.Hotel', related_name='contacts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.hotel.name}"
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']

# This model is used to store newsletter subscriptions.
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    hotels = models.ManyToManyField('hotels.Hotel', related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-created_at']

# This model is used to store feedback from users.
class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    hotel = models.ForeignKey('hotels.Hotel', related_name='feedbacks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} - {self.hotel.name}"
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    hotels = models.ManyToManyField('hotels.Hotel', related_name='privacy_policies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"
        ordering = ['-created_at']
        
class TermsAndConditions(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    hotels = models.ManyToManyField('hotels.Hotel', related_name='terms_and_conditions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Terms and Conditions"
        verbose_name_plural = "Terms and Conditions"
        ordering = ['-created_at']

class Sitemap(models.Model):
    url = models.URLField()
    hotels = models.ManyToManyField('hotels.Hotel', related_name='sitemaps')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    class Meta:
        verbose_name = "Sitemap"
        verbose_name_plural = "Sitemaps"
        ordering = ['-created_at']

class HotelArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_articles/', null=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, null=True)
    tags = models.CharField(max_length=255, blank=True)
    hotels = models.ManyToManyField('hotels.Hotel', related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/articles/{self.slug}/"
    
    class Meta:
        verbose_name = "Hotel Article"
        verbose_name_plural = "Hotel Articles"
        ordering = ['-created_at']

# Career model
class Career(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('training', 'Training'),
    ]

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='careers'
    )
    job_title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    job_description = models.TextField(max_length=70)
    job_requirements = models.TextField(
        help_text="Separate each requirement with a line break",
        blank=True,
        null=True
    )
    job_location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPES,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"
        ordering = ['-created_at']
        unique_together = ('hotel', 'slug')  # ✅ Slug must be unique per hotel

    def __str__(self):
        return f"{self.job_title} @ {self.hotel.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.job_title)
            unique_slug = base_slug
            counter = 1
            while Career.objects.filter(hotel=self.hotel, slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

# This model is used to store career applications.
class CareerApplication(models.Model):
    career = models.ForeignKey('Career', on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    resume = models.FileField(upload_to='careers/resumes/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.career.job_title}"