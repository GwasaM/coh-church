from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from .models import CustomUser, Event, BlogPost, Carousel, NewsletterSubscription, GeographicLocation, Page, Video, Testimonial, TeamMember, Mail, ChurchNews, ContactMessage, SocialMediaLink


# CustomUserAdmin configuration
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_pastor', 'is_event_uploader']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_pastor', 'is_event_uploader')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_pastor', 'is_event_uploader'),
        }),
    )
    filter_horizontal = ()

# Register the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'description')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title', 'content')

#@admin.register(NewsletterSubscription)
# NewsletterSubscriptionAdmin(admin.ModelAdmin):
 #   list_display = ('email', 'subscribed_at')

@admin.register(GeographicLocation)
class GeographicLocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude')

#@admin.register(Page)
#class PageAdmin(admin.ModelAdmin):
#    list_display = ('title', 'slug')
#    prepopulated_fields = {'slug': ('title',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'content']
    list_filter = ['page_type']

admin.site.register(Page, PageAdmin)

#Another way to register models
admin.site.register(Video)
admin.site.register(Testimonial)
admin.site.register(TeamMember)
admin.site.register(Mail)
admin.site.register(ChurchNews)
#admin.site.register(ContactMessage)


class ContactMessageAdmin(admin.ModelAdmin):
    # Disable all the modification options by overriding the methods
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Optionally, limit the displayed fields if you don't want to show all
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')

# Register the model with the customized admin class
admin.site.register(ContactMessage, ContactMessageAdmin)


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url']
    list_filter = ['platform']
    search_fields = ['url']


class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return 
    
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)