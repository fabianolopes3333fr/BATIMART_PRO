from .models import PageConfig, SiteConfig

def page_config(request):
    configs = PageConfig.objects.all()
    return {config.page_name: config for config in configs}

def site_config(request):
    config = SiteConfig.objects.first()
    return {'site_config': config}