from django.db import models

class BusinessProfile(models.Model):
    name = models.CharField(max_length=100)  # Name of the business
    description = models.TextField()  # Description of the business
    services_offered = models.TextField()  # Services offered by the business
    location = models.CharField(max_length=255)  # Location of the business
    avg_rating = models.FloatField(null=True, blank=True)  # Average rating (optional)

    def __str__(self):
        return self.name  # Return the business name when displayed in the admin panel
