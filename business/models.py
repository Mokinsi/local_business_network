from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from datetime import timedelta


class BusinessProfile(models.Model):
    """Model representing a business profile."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_profiles')
    business_name = models.CharField(max_length=255, default="Unnamed Business")
    services_offered = models.TextField()
    working_hours = models.CharField(max_length=100)  # e.g., "Mon-Fri: 9 AM - 5 PM"
    location = models.CharField(max_length=255, default="Unknown Location")
    contact_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[1-9]\d{9,14}$', 'Enter a valid international phone number')]
    )
    contact_whatsapp = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[1-9]\d{9,14}$', 'Enter a valid international WhatsApp number')]
    )
    contact_email = models.EmailField()
    website = models.URLField(blank=True, null=True)  # Optional field for website
    overview_picture = models.ImageField(upload_to='business_overviews/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Business Profiles"

    def __str__(self):
        return self.business_name

    def average_rating(self):
        """Calculate and return the average rating, capping at 5."""
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return min(avg_rating, 5)


class Review(models.Model):
    """Model representing a review for a business profile."""

    business = models.ForeignKey(BusinessProfile, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} Stars for {self.business.business_name}"


class BusinessAnalytics(models.Model):
    """Model to track analytics for a business profile."""

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Business Analytics"

    def increment_views(self):
        """Increment view count each time the profile is viewed."""
        self.views += 1
        self.save(update_fields=['views'])

    def increment_clicks(self):
        """Increment click count each time a tracked action is clicked."""
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def reset_daily_views(self):
        """Reset daily view count if a new day starts."""
        if timezone.now().date() != self.last_viewed.date():
            self.views = 0
            self.save(update_fields=['views'])

    def reset_monthly_views(self):
        """Reset monthly view count if a new month starts."""
        if timezone.now().month != self.last_viewed.month:
            self.views = 0
            self.save(update_fields=['views'])


class Message(models.Model):
    """Model representing a message sent to a business profile."""

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} to {self.business.business_name}"


class ChatMessage(models.Model):
    """Model for a chat system between users."""

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, null=True, blank=True)  # Made nullable
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Added this field

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.message[:50]}"


def get_business_data():
    """Retrieve business data for all business profiles."""
    businesses = BusinessProfile.objects.all()
    return [
        {
            'id': business.id,
            'name': business.business_name,
            'services': business.services_offered,
            'location': business.location
        }
        for business in businesses
    ]


class BusinessOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.business_name