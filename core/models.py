from django.db import models

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
    image = models.ImageField(upload_to='hotel_articles/', null=True, blank=True)
    hotels = models.ManyToManyField('hotels.Hotel', related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Hotel Article"
        verbose_name_plural = "Hotel Articles"
        ordering = ['-created_at']