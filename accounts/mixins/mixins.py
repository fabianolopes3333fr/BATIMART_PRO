# mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages

class EmailVerificationRequiredMixin(LoginRequiredMixin):
    """
    Mixin para verificar se o email do usuário foi verificado
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified:
            messages.warning(
                request,
                _('Veuillez vérifier votre e-mail avant de continuer.')
            )
            return redirect('verification-required')
        return super().dispatch(request, *args, **kwargs)

class StaffRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é staff
    """
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('admin:login')
        raise PermissionDenied(
            _("Vous n'avez pas la permission d'accéder à cette page.")
        )

class SuperUserRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é superusuário
    """
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('admin:login')
        raise PermissionDenied(
            _("Vous n'avez pas la permission d'accéder à cette page.")
        )

class ProfileOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar se o usuário é dono do perfil
    """
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied(
            _("Vous n'avez pas la permission d'accéder à ce profil.")
        )