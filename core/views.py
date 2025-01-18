from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.cache import cache
from .forms import ContactForm
from django.views.decorators.cache import cache_page
from .models import Client, Page, Section, Menu, Theme, Testimonial

def get_client(request, client_slug=None):
    if client_slug:
        return get_object_or_404(Client, slug=client_slug, is_active=True)
    elif request.user.is_authenticated and hasattr(request.user, 'client'):
        return request.user.client
    else:
        # Retorna o primeiro cliente ativo se nenhum for especificado
        return Client.objects.filter(is_active=True).first()

@cache_page(60 * 15)  # Cache for 15 minutes
def render_page(request, client_slug, page_slug=None):
    client = get_client(request, client_slug)
    if not client:
        raise Http404("No active client found")

    if page_slug:
        page = get_object_or_404(Page, client=client, slug=page_slug)
    else:
        page = get_object_or_404(Page, client=client, is_home=True)
    
    sections = Section.objects.filter(page=page).order_by('order')
    menu_items = Menu.objects.filter(client=client, parent=None)
    theme = Theme.objects.get(client=client)
    
    context = {
        'client': client,
        'page': page,
        'sections': sections,
        'menu_items': menu_items,
        'theme': theme,
    }
    
    return render(request, 'page.html', context)


def home(request, client_slug=None):
    context = {}
    if client_slug:
        client = get_object_or_404(Client, slug=client_slug)
        context['client'] = client
    
    # Verifique se o usuário foi redirecionado devido a inatividade
    if request.GET.get('session_expired'):
        context['session_expired'] = True
    
    return render(request, 'home.html', context)

def page(request, page_slug, client_slug=None):
    return render_page(request, client_slug, page_slug)

def services(request):
    # Lógica para a view de serviços
    return render(request, 'services.html')

def projects(request):
    # Lógica para a view de projetos
    return render(request, 'projects.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

def about(request):
    return render(request, 'about.html')

def testimonials(request, client_slug=None):
    client = get_object_or_404(Client, slug=client_slug, is_active=True)
    testimonials = Testimonial.objects.filter(client=client, is_active=True)
    menu_items = Menu.objects.filter(client=client, parent=None)
    theme = Theme.objects.get(client=client)

    context = {
        'client': client,
        'testimonials': testimonials,
        'menu_items': menu_items,
        'theme': theme,
    }

    return render(request, 'testimonials.html')