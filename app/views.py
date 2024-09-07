from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import BlogPost
from .models import Testimonial
from .models import Video
from .models import Carousel
from .models import NewsletterSubscription
from .forms import ContactForm
from .models import SocialMediaLink
from .models import Page

# Create your views here.
def home(request):
     testimonials = Testimonial.objects.all().order_by('date')[:3]
     videos = Video.objects.all().order_by('uploaded_at')[:3]
     carousels = Carousel.objects.all().order_by('published_date')#[:5]

     context = {
        'testimonials': testimonials,
        'videos': videos,
        'carousels': carousels,
     }
     return render(request, 'app/home.html', context)

def about_us(request):
     context = {'key':'value'}
     return render(request, 'app/about.html', context)

def blog(request):
    # Retrieve the most recent blog post as the featured post
    featured_post = BlogPost.objects.order_by('-published_date').first()

    # Retrieve the 5 most recent posts, excluding the featured post
    recent_posts = BlogPost.objects.exclude(id=featured_post.id).order_by('-published_date')[:5]

    context = {
        'featured_post': featured_post,
        'recent_posts': recent_posts,
    }

    return render(request, 'app/blog.html', context)


def mission(request):
     return render(request, 'app/mission.html', {'key':'value'})
def contact(request):
     return render(request, 'app/contact.html', {'key':'value'})

def blog_post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'app/blog_post_detail.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the contact message to the database
        return redirect('contact')  # Redirect to a success page or similar
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form})


def newsletter_subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # Check if email already exists in the database
                if NewsletterSubscription.objects.filter(email=email).exists():
                    messages.warning(request, 'You are already subscribed to our newsletter.')
                else:
                    # Save the email to the database
                    subscription = NewsletterSubscription(email=email, subscribed_at=timezone.now())
                    subscription.save()
                    messages.success(request, 'Thank you for subscribing to our newsletter!')
            except Exception as e:
                messages.error(request, 'An error occurred while subscribing. Please try again.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        
        return redirect('home')  # Redirect to home or another page after form submission

    return render(request, 'home.html')


def render_page(request, slug):
    # Assuming you have a 'slug' field in your Page model to identify different pages
    page = get_object_or_404(Page, slug=slug)
    return render(request, f'{slug}.html', {'page_content': page})
