from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ConfigStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin pour s'assurer que l'utilisateur est un membre du personnel pour accéder aux vues de configuration.
    """
    redirect_url = 'admin:index'  # Redirige vers l'index de l'admin si l'accès est refusé
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return getattr(self.request.user, 'is_staff', False)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, _("Vous n'avez pas les permissions nécessaires pour accéder aux configurations du site."))
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return self.redirect_url if hasattr(self, 'redirect_url') else 'admin:index'

class ConfigSuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin pour s'assurer que l'utilisateur est un superutilisateur pour accéder aux vues de configuration sensibles.
    """
    redirect_url = 'admin:index'  # Redirige vers l'index de l'admin si l'accès est refusé
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def test_func(self):
        return getattr(self.request.user, 'is_superuser', False)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, _("Seuls les superutilisateurs peuvent accéder à cette configuration."))
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return self.redirect_url if hasattr(self, 'redirect_url') else 'admin:index'