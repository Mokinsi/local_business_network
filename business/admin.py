from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import BusinessProfile, Review, BusinessAnalytics, Message, ChatMessage

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'location', 'contact_phone', 'get_services_short')
    list_filter = ('location',)
    search_fields = ('business_name', 'user__username', 'location', 'services_offered')
    actions = ['delete_selected_businesses']
    
    def get_services_short(self, obj):
        """Display shortened version of services offered"""
        return obj.services_offered[:50] + '...' if len(obj.services_offered) > 50 else obj.services_offered
    get_services_short.short_description = 'Services'

    def delete_selected_businesses(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} businesses.")
    delete_selected_businesses.short_description = "Delete selected businesses"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('business__business_name', 'user__username', 'comment')
    date_hierarchy = 'created_at'

class BusinessAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('business', 'views', 'clicks', 'last_viewed')
    readonly_fields = ('last_viewed',)
    list_filter = ('last_viewed',)

class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'business_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    actions = ['delete_users_and_businesses']
    
    def business_count(self, obj):
        return obj.business_profiles.count()
    business_count.short_description = 'Businesses'
    
    def delete_users_and_businesses(self, request, queryset):
        count = queryset.count()
        business_count = sum(user.business_profiles.count() for user in queryset)
        for user in queryset:
            user.business_profiles.all().delete()
            user.delete()
        self.message_user(request, f"Deleted {count} users and {business_count} associated businesses.")
    delete_users_and_businesses.short_description = "Delete users and their businesses"

# System Statistics View
class SystemStatsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/system_stats.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'total_businesses': BusinessProfile.objects.count(),
            'total_users': User.objects.count(),
            'total_reviews': Review.objects.count(),
            'total_messages': Message.objects.count(),
            'total_chats': ChatMessage.objects.count(),
        })
        return super().changelist_view(request, extra_context)
    
    def has_add_change_delete_permission(self, request, obj=None):
        return False

# Create proxy model for system stats
class SystemStats(BusinessProfile):
    class Meta:
        proxy = True
        verbose_name_plural = "System Statistics"

# Register models with default admin site
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BusinessAnalytics, BusinessAnalyticsAdmin)
admin.site.register(Message)
admin.site.register(ChatMessage)
admin.site.register(SystemStats, SystemStatsAdmin)