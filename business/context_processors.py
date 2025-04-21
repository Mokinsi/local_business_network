from .models import BusinessOwner  # Import your business owner model

def business_owners_context(request):
    return {'business_owners': BusinessOwner.objects.all()}

from .models import BusinessProfile

def business_context(request):
    """Context processor to make businesses available in all templates."""
    if request.user.is_authenticated:
        businesses = BusinessProfile.objects.filter(user=request.user)
    else:
        businesses = None  # Empty queryset for non-authenticated users

    return {'businesses': businesses}
