from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import render_page

urlpatterns = [
    path('', views.home, name="home"),
    path('about-us/', views.about_us, name='about_us'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog_post_detail, name='blog_post_detail'),
    path('mission/', views.mission, name='mission'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.newsletter_subscription, name='newsletter_subscription'),

    # The slug-based pattern should be last
    path('<slug:slug>/', render_page, name='page_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
