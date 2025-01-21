# config/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

from .models import SiteConfig, Menu, BancoImagens
from .forms import SiteConfigForm, MenuForm, MediaLibraryForm
from .mixins import StaffRequiredMixin

@method_decorator(staff_member_required, name='dispatch')
class SiteConfigUpdateView(UpdateView):
    model = SiteConfig
    form_class = SiteConfigForm
    template_name = 'config/site_config_form.html'
    success_url = reverse_lazy('site-config')

    def get_object(self):
        config = cache.get('site_config')
        if not config:
            config, created = SiteConfig.objects.get_or_create(pk=1)
            cache.set('site_config', config)
        return config

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Les paramètres du site ont été mis à jour.')
        )
        cache.delete('site_config')
        return super().form_valid(form)

class MenuListView(StaffRequiredMixin, ListView):
    model = Menu
    template_name = 'config/menu_list.html'
    context_object_name = 'menus'
    ordering = ['order']

class MenuCreateView(StaffRequiredMixin, CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'config/menu_form.html'
    success_url = reverse_lazy('menu-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Le menu a été créé avec succès.')
        )
        return super().form_valid(form)

class MenuUpdateView(StaffRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'config/menu_form.html'
    success_url = reverse_lazy('menu-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Le menu a été mis à jour.')
        )
        return super().form_valid(form)

class MenuDeleteView(StaffRequiredMixin, DeleteView):
    model = Menu
    template_name = 'config/menu_confirm_delete.html'
    success_url = reverse_lazy('menu-list')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('Le menu a été supprimé.')
        )
        return super().delete(request, *args, **kwargs)

class MediaLibraryListView(StaffRequiredMixin, ListView):
    model = BancoImagens
    template_name = 'config/media_list.html'
    context_object_name = 'medias'
    paginate_by = 20

class MediaLibraryCreateView(StaffRequiredMixin, CreateView):
    model = BancoImagens
    form_class = MediaLibraryForm
    template_name = 'config/media_form.html'
    success_url = reverse_lazy('media-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Le média a été ajouté avec succès.')
        )
        return super().form_valid(form)