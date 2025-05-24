from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q, Prefetch
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Value
from django.db.models.functions import Coalesce 
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import BusinessProfile, Review, BusinessAnalytics, Message, User
from .forms import CustomUserCreationForm, BusinessProfileForm, ReviewForm, MessageForm
from .models import BusinessProfile, ChatMessage, User

def index(request):
    """Homepage view displaying business profiles based on search criteria, sorted by rating."""
    businesses = BusinessProfile.objects.none()  # Default to an empty queryset

    if request.method == 'POST':
        location = request.POST.get('location', '').strip()
        service = request.POST.get('service', '').strip()

        # Create a base query with filters
        filters = Q()
        if location:
            filters &= Q(location__icontains=location)  # Case-insensitive search
        if service:
            filters &= Q(services_offered__icontains=service)  # Case-insensitive search

        # Filter businesses and order them by average rating in descending order
        businesses = (
            BusinessProfile.objects
            .filter(filters)
            .annotate(avg_rating=Coalesce(Avg('reviews__rating'), Value(0.0)))  # Replace NULL with 0.0
            .order_by('-avg_rating')  # Sort in descending order
        )

        # Paginate the results (10 businesses per page)
        paginator = Paginator(businesses, 10)
        page_number = request.GET.get('page')
        businesses = paginator.get_page(page_number)

    return render(request, 'business/index.html', {'businesses': businesses})

def signup(request):
    """User signup view with simplified password requirements."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend to use when logging in the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Signup successful! Please proceed to create your business profile.")
            return redirect('create_business')  # Redirect to the create business profile page
        else:
            messages.error(request, "Signup failed. Please check the highlighted fields and try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'business/signup.html', {
        'form': form,
        'google_signup_url': reverse('google_signup'),  # For Google signup integration
    })

def google_signup(request):
    """View to handle Google signup."""
    messages.success(request, "Google signup not implemented yet.")
    return redirect('index')

def login_view(request):
    """User login view that handles multiple profiles."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            
            # Check for any business profiles
            if BusinessProfile.objects.filter(user=user).exists():
                return redirect('profile')
            else:
                messages.warning(request, "You don't have a business profile yet. Please create one.")
                return redirect('create_business')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'business/login.html')

def business_dashboard(request, business_id):
    """View for business analytics dashboard."""
    business = get_object_or_404(BusinessProfile, id=business_id, user=request.user)
    
    # Get or create analytics and increment views
    analytics, _ = BusinessAnalytics.objects.get_or_create(business=business)
    analytics.increment_views()
    
    # Get real analytics data (last 30 days)
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    daily_data = BusinessAnalytics.objects.filter(
        business=business,
        last_viewed__date__gte=thirty_days_ago
    ).order_by('last_viewed')
    
    # Prepare chart data
    analytics_data = {
        "labels": [entry.last_viewed.strftime("%b %d") for entry in daily_data],
        "views": [entry.views for entry in daily_data],
        "clicks": [entry.clicks for entry in daily_data],
    }

    return render(request, "business/dashboard.html", {
        "business": business,
        "analytics": analytics,
        "analytics_data": analytics_data
    })
    
@login_required
def profile(request):
    """User profile view that handles multiple profiles."""
    try:
        # Get all profiles for the user
        profiles = BusinessProfile.objects.filter(user=request.user)
        
        if not profiles.exists():
            messages.warning(request, "No business profile found. Please create one.")
            return redirect('create_business')
            
        # If multiple profiles, use the first one (since we don't have created_at)
        # Alternatively, you could add a created_at field to your model
        business = profiles.first()
        
        if profiles.count() > 1:
            messages.warning(request, "Multiple profiles detected. Using one of them.")
            # Consider adding admin notification here
            
        if request.method == 'POST':
            business.delete()
            messages.success(request, "Your business profile has been deleted successfully.")
            return redirect('index')

        return render(request, 'business/profile.html', {'business': business})
        
    except Exception as e:
        messages.error(request, f"Error accessing profile: {str(e)}")
        return redirect('index')
    
@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

@login_required
def create_business(request):
    """View for creating a new business profile."""
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            BusinessAnalytics.objects.create(business=business)
            messages.success(request, "Business profile created successfully.")
            return redirect('view_business_profile', business_id=business.id)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = BusinessProfileForm()
    return render(request, 'business/create_business.html', {'form': form})

@login_required
def update_business(request, business_id):
    """View for updating an existing business profile."""
    business = get_object_or_404(BusinessProfile, id=business_id, user=request.user)
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, "Business profile updated successfully.")
            return redirect('view_business_profile', business_id=business.id)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = BusinessProfileForm(instance=business)
    return render(request, 'business/update_business.html', {'form': form, 'business': business})


def view_business_profile(request, business_id):
    """View for displaying a business profile and handling messages."""
    business = get_object_or_404(BusinessProfile, pk=business_id)

    # Initialize message form
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.business = business
            message.user = request.user
            message.save()
            messages.success(request, "Message sent successfully.")  # Provide feedback
            return redirect('view_business_profile', business_id=business.id)
    else:
        message_form = MessageForm()

    messages = Message.objects.filter(business=business).order_by('-created_at')  # Change to fetch messages by business

    return render(request, 'business/view_business_profile.html', {
        'business': business,
        'message_form': message_form,
        'messages': messages
    })


def submit_review(request, business_id):
    """Allow authenticated users to submit a review for a business."""
    business = get_object_or_404(BusinessProfile, id=business_id)
    
    if business.user == request.user:
        messages.warning(request, "You cannot submit a review for your own business.")
        return redirect('view_business_profile', business_id=business.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.business = business
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('view_business_profile', business_id=business.id)
    else:
        form = ReviewForm()

    return render(request, 'business/submit_review.html', {'form': form, 'business': business})

@login_required
def increment_clicks(request, business_id):
    """Track clicks on a business profile."""
    if request.method == "POST":  # Ensure it's a POST request
        business = get_object_or_404(BusinessProfile, id=business_id)
        
        analytics, _ = BusinessAnalytics.objects.get_or_create(business=business)
        analytics.clicks += 1
        analytics.last_clicked = timezone.now()
        analytics.save()

        return JsonResponse({"success": True, "clicks": analytics.clicks})  # Return JSON response

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def delete_business(request, business_id):
    """View for deleting a business profile."""
    business = get_object_or_404(BusinessProfile, id=business_id, user=request.user)
    if request.method == 'POST':
        business.delete()
        messages.success(request, "Your business profile has been deleted successfully.")
        return redirect('index')
    return redirect('view_business_profile', business_id=business_id)


@login_required
def chat_view(request, business_owner_id):
    """Displays the chat interface between the logged-in user and the business owner."""
    business_owner = get_object_or_404(User, id=business_owner_id)

    # Retrieve chat messages between logged-in user and business owner
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, recipient=business_owner) |
        Q(sender=business_owner, recipient=request.user)
    ).select_related('sender', 'recipient').order_by('timestamp')  # Oldest messages first

    # Bulk update unread messages for better efficiency
    ChatMessage.objects.filter(
        recipient=request.user, sender=business_owner, read=False
    ).update(read=True)

    return render(request, 'chat/chat.html', {
        'business_owner': business_owner,
        'messages': messages,
    })
    
@login_required
@csrf_exempt
def fetch_messages(request, business_owner_id):
    """Fetch new messages for polling updates."""
    try:
        business_owner = get_object_or_404(User, id=business_owner_id)

        last_message_id = request.GET.get('last_message_id', 0)

        # Fetch only messages after last_message_id
        messages_qs = ChatMessage.objects.filter(
            Q(sender=request.user, recipient=business_owner) |
            Q(sender=business_owner, recipient=request.user),
            id__gt=last_message_id  # Get only new messages
        ).select_related('sender', 'recipient').order_by('timestamp')  # Oldest first

        messages_data = [
            {
                'id': msg.id,
                'sender': msg.sender.username,
                'recipient': msg.recipient.username,
                'message': msg.message,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for msg in messages_qs
        ]

        return JsonResponse({'messages': messages_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def recent_chats(request):
    """Fetch recent chat contacts."""
    # Get the most recent message per conversation
    recent_conversations = (
        ChatMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values("sender", "recipient")
        .annotate(last_timestamp=Max("timestamp"))
        .order_by("-last_timestamp")
    )

    unique_conversations = []
    seen_users = set()

    for convo in recent_conversations:
        other_user_id = convo["recipient"] if convo["sender"] == request.user.id else convo["sender"]

        if other_user_id not in seen_users:
            seen_users.add(other_user_id)
            other_user = get_object_or_404(User, id=other_user_id)

            last_message = (
                ChatMessage.objects.filter(
                    Q(sender=request.user, recipient=other_user) |
                    Q(sender=other_user, recipient=request.user)
                )
                .order_by("-timestamp")
                .first()
            )

            unique_conversations.append({
                "id": other_user.id,
                "username": other_user.username,
                "last_message": last_message.message if last_message else "No messages yet",
                "timestamp": last_message.timestamp.strftime('%Y-%m-%d %H:%M:%S') if last_message else "",
            })

    return JsonResponse(unique_conversations, safe=False)


@login_required
@csrf_exempt
def send_message(request, business_owner_id):
    """Handles sending messages via AJAX."""
    if request.method == 'POST':
        try:
            recipient = get_object_or_404(User, id=business_owner_id)

            # Ensure data is received as JSON
            data = json.loads(request.body)
            message_text = data.get("message", "").strip()

            if not message_text:
                return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

            message = ChatMessage.objects.create(
                sender=request.user,
                recipient=recipient,
                message=message_text
            )

            return JsonResponse({
                'id': message.id,
                'sender': message.sender.username,
                'recipient': message.recipient.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)