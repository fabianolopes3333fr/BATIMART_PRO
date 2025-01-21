# profiles/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, HttpRequest
from typing import Any, Optional
from .models import ClientProfile

class ProfileOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar se o usuário atual é o dono do perfil.
    Requer que a view tenha um método get_object().
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Sobrescreve dispatch para garantir que o usuário está autenticado"""
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('Veuillez vous connecter pour accéder à cette page.')
            )
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def test_func(self) -> bool:
        """
        Verifica se o usuário atual é o dono do perfil.
        Requer que a view tenha um método get_object().
        """
        try:
            obj = self.get_object()  # type: ignore
            if isinstance(obj, ClientProfile):
                return obj.user == self.request.user  # type: ignore
            elif hasattr(obj, 'profile'):
                return obj.profile.user == self.request.user  # type: ignore
            return False
        except (AttributeError, TypeError):
            return False


    def handle_no_permission(self) -> HttpResponse:
        """
        Chamado quando o usuário não tem permissão para acessar a view.
        """
        if not self.request.user.is_authenticated:  # type: ignore
            messages.error(
                self.request,  # type: ignore
                _('Veuillez vous connecter pour accéder à cette page.')
            )
            return redirect('accounts:login')
        
        messages.error(
            self.request,  # type: ignore
            _('Vous n\'avez pas la permission d\'accéder à ce profil.')
        )
        return redirect('profiles:profile-list')  # URL nomeada com namespace


    def get_permission_denied_message(self) -> str:
        """
        Retorna a mensagem quando o acesso é negado
        """
        return _('Vous n\'avez pas la permission d\'accéder à ce profil.')