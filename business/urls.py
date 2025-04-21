from django.urls import path
from . import views
from .views import business_dashboard
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_business/', views.create_business, name='create_business'),
    path('update_business/<int:business_id>/', views.update_business, name='update_business'),
    path('view_business_profile/<int:business_id>/', views.view_business_profile, name='view_business_profile'),
    path('submit_review/<int:business_id>/', views.submit_review, name='submit_review'),
    path('google_signup/', views.google_signup, name='google_signup'),
    path('dashboard/<int:business_id>/', business_dashboard, name='business_dashboard'),
    path('delete_business/<int:business_id>/', views.delete_business, name='delete_business'),
    path('chat/<int:business_owner_id>/', views.chat_view, name='chat'),
    path('business/chat/<int:business_owner_id>/', views.chat_view, name='chat_business'),
    path('dashboard/<int:business_id>/', views.business_dashboard, name='dashboard'),
    path('dashboard/<int:business_id>/', views.business_dashboard, name='business_dashboard'),




    # ✅ Chat System
    path('chat/<int:business_owner_id>/', views.chat_view, name='chat'),
    path('fetch_messages/<int:business_owner_id>/', views.fetch_messages, name='fetch_messages'),  # ✅ Fetch messages
    path('send_message/<int:business_owner_id>/', views.send_message, name='send_message'),  # ✅ Send message
]
