from django.contrib.sites.models import Site


def site(request):
    return {
        'site': Site.objects.all()[0],
    }
