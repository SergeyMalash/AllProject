import os


def site_host(request):
    return {'SITE_HOST': os.getenv('SITE_HOST')}
