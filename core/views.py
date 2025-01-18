from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Client, Page, Section, Menu, Theme

def get_client(request, client_slug=None):
    if client_slug:
        return get_object_or_404(Client, slug=client_slug)
    elif request.user.is_authenticated:
        return request.user.client
    else:
        raise Http404("Client not found")

@cache_page(60 * 15)  # Cache for 15 minutes
def render_page(request, client_slug=None, page_slug='home'):
    client = get_client(request, client_slug)
    page = get_object_or_404(Page, client=client, slug=page_slug, is_active=True)

    sections = Section.objects.filter(page=page)
    menu_items = Menu.objects.filter(client=client, parent=None)
    theme = Theme.objects.get(client=client)

    context = {
        'client': client,
        'page': page,
        'sections': sections,
        'menu_items': menu_items,
        'theme': theme,
    }

    return render(request, 'core/page.html', context)

def home(request, client_slug=None):
    return render_page(request, client_slug)

def page(request, page_slug, client_slug=None):
    return render_page(request, client_slug, page_slug)
