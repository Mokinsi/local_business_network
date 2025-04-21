from django.shortcuts import render
from django.http import JsonResponse
from ai_features.models import BusinessProfile
from ai_features.recommendations import recommend_businesses_transformer, recommend_businesses_tfidf

def get_business_data():
    """
    Fetch business data from the database for AI-driven recommendations.
    
    Returns:
        list of dict: Business details including ID, name, services, and location.
    """
    businesses = BusinessProfile.objects.all()
    data = [
        {
            'id': b.id,
            'name': b.name,
            'services_offered': b.services_offered,
            'location': b.location,
            'avg_rating': b.avg_rating,  # Ensure avg_rating exists in your model
        }
        for b in businesses
    ]
    return data

def recommend_view(request):
    user_query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    method = request.GET.get('method', 'transformer')

    print(f"🔍 User Query: {user_query}")
    print(f"📍 Location: {location}")
    print(f"🛠️ Method: {method}")

    business_data = get_business_data()
    print(f"📊 Business Data: {business_data}")

    if method == 'tfidf':
        recommendations = recommend_businesses_tfidf(user_query, location, business_data)
    else:
        recommendations = recommend_businesses_transformer(user_query, location, business_data)

    print(f"✅ Recommendations: {recommendations}")

    return JsonResponse({'recommendations': recommendations})
