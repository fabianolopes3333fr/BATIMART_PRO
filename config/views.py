# config/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from .models import SiteConfig, Menu, BancoImagens, Page, Redirect
from .forms import SiteConfigForm, MenuForm, BancoImagensForm, PageForm, RedirectForm
from .mixins import ConfigStaffRequiredMixin, ConfigSuperUserRequiredMixin

@method_decorator(staff_member_required, name='dispatch')
class SiteConfigUpdateView(ConfigSuperUserRequiredMixin, UpdateView):
    model = SiteConfig
    form_class = SiteConfigForm
    template_name = 'config/site_config_form.html'
    success_url = reverse_lazy('admin:index')

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


class MenuListView(ConfigStaffRequiredMixin, ListView):
    model = Menu
    template_name = 'config/menu_list.html'
    context_object_name = 'menus'

class MenuCreateView(ConfigStaffRequiredMixin, CreateView):
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

class MenuUpdateView(ConfigStaffRequiredMixin, UpdateView):
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

class MenuDeleteView(ConfigStaffRequiredMixin, DeleteView):
    model = Menu
    template_name = 'config/menu_confirm_delete.html'
    success_url = reverse_lazy('menu-list')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('Le menu a été supprimé.')
        )
        return super().delete(request, *args, **kwargs)

class BancoImagensListView(ConfigStaffRequiredMixin, ListView):
    model = BancoImagens
    template_name = 'config/banco_imagens_list.html'
    context_object_name = 'images'
    paginate_by = 20

class BancoImagensCreateView(ConfigStaffRequiredMixin, CreateView):
    model = BancoImagens
    form_class = BancoImagensForm
    template_name = 'config/banco_imagens_form.html'
    success_url = reverse_lazy('banco-imagens-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('L\'image a été ajoutée avec succès à la banque d\'images.')
        )
        return super().form_valid(form)

class BancoImagensUpdateView(ConfigStaffRequiredMixin, UpdateView):
    model = BancoImagens
    form_class = BancoImagensForm
    template_name = 'config/banco_imagens_form.html'
    success_url = reverse_lazy('banco-imagens-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('L\'image a été mise à jour avec succès.')
        )
        return super().form_valid(form)

class BancoImagensDeleteView(ConfigStaffRequiredMixin, DeleteView):
    model = BancoImagens
    template_name = 'config/banco_imagens_confirm_delete.html'
    success_url = reverse_lazy('banco-imagens-list')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('L\'image a été supprimée avec succès de la banque d\'images.')
        )
        return super().delete(request, *args, **kwargs)
    
    
class PageListView(ConfigStaffRequiredMixin, ListView):
    model = Page
    template_name = 'config/page_list.html'
    context_object_name = 'pages'

class PageCreateView(ConfigStaffRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'config/page_form.html'
    success_url = reverse_lazy('page-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, _('La page a été créée avec succès.'))
        return super().form_valid(form)

class PageUpdateView(ConfigStaffRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'config/page_form.html'
    success_url = reverse_lazy('page-list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, _('La page a été mise à jour.'))
        return super().form_valid(form)

class PageDeleteView(ConfigStaffRequiredMixin, DeleteView):
    model = Page
    template_name = 'config/page_confirm_delete.html'
    success_url = reverse_lazy('page-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('La page a été supprimée.'))
        return super().delete(request, *args, **kwargs)

class RedirectListView(ConfigStaffRequiredMixin, ListView):
    model = Redirect
    template_name = 'config/redirect_list.html'
    context_object_name = 'redirects'

class RedirectCreateView(ConfigStaffRequiredMixin, CreateView):
    model = Redirect
    form_class = RedirectForm
    template_name = 'config/redirect_form.html'
    success_url = reverse_lazy('redirect-list')

    def form_valid(self, form):
        messages.success(self.request, _('La redirection a été créée avec succès.'))
        return super().form_valid(form)

class RedirectUpdateView(ConfigStaffRequiredMixin, UpdateView):
    model = Redirect
    form_class = RedirectForm
    template_name = 'config/redirect_form.html'
    success_url = reverse_lazy('redirect-list')

    def form_valid(self, form):
        messages.success(self.request, _('La redirection a été mise à jour.'))
        return super().form_valid(form)

class RedirectDeleteView(ConfigStaffRequiredMixin, DeleteView):
    model = Redirect
    template_name = 'config/redirect_confirm_delete.html'
    success_url = reverse_lazy('redirect-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('La redirection a été supprimée.'))
        return super().delete(request, *args, **kwargs)