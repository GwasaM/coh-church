from .models import SocialMediaLink

def social_links(request):
    links = SocialMediaLink.objects.all()
    return {'social_links': links}