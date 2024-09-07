from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_pastor = models.BooleanField(default=False)
    is_event_uploader = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_posts/', blank=False, null=False)

    def __str__(self):
        return self.title
    

class Carousel(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the slide.")
    content = models.TextField(blank=True, help_text="Optional description for the slide.")
    image = models.ImageField(upload_to='carousel_images/', help_text="Image for the carousel slide.")
    is_active = models.BooleanField(default=False, help_text="Set to true to make this slide the first one displayed.")
    order = models.PositiveIntegerField(default=0, help_text="Order of the slide in the carousel.")
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

class GeographicLocation(models.Model):
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.address


class Page(models.Model):
    TITLE_CHOICES = [
        ('base', 'Base Page'),
        ('contact', 'Contact Page'),
        ('mission', 'Mission Page'),
        ('home', 'Home Page'),
        ('about-us', 'About Page'),
        # Add other page types as needed
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='page_photos/', null=True, blank=True)
    page_type = models.CharField(max_length=50, choices=TITLE_CHOICES, null=True)
    
    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()  # For embedded videos
    thumbnail = models.ImageField(upload_to='thumbnails/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    company = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name
    
    
class TeamMember(models.Model):
    POSITION_CHOICES = [
        ('Pastor', 'Pastor'),
        ('Assistant Pastor', 'Assistant Pastor'),
        ('Elder', 'Elder'),
        ('Deacon', 'Deacon'),
        ('Choir Leader', 'Choir Leader'),
        ('Youth Leader', 'Youth Leader'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Usher', 'Usher'),
        ('Member', 'Member'),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    
class Mail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"
    
class ChurchNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('google', 'Google'),
        ('linkedin', 'LinkedIn'),
        # Add more platforms if needed
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=200)
    icon_class = models.CharField(max_length=100, default='bi')

    def __str__(self):
        return f"{self.get_platform_display()}"

# Example of using the model:
# facebook = SocialMediaLink(platform='facebook', url='https://facebook.com/yourpage', icon_class='bi bi-facebook')


