# mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

class StaffRequiredMixin(UserPassesTestMixin):
    """Garante que apenas staff pode acessar a view"""
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Vous n'avez pas la permission d'accéder à cette page.")
        )
        return redirect('login')

class ProfileOwnerRequiredMixin(UserPassesTestMixin):
    """Garante que apenas o dono do perfil pode acessar"""
    def test_func(self):
        obj = self.get_object()
        return obj.profile.user == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Vous n'avez pas la permission d'accéder à ce contenu.")
        )
        return redirect('profile')

class AuditableMixin:
    """Adiciona campos de auditoria aos modelos"""
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = self.request.user
        self.modified_by = self.request.user
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

class TransactionMixin:
    """Garante transações atômicas em operações de banco"""
    @transaction.atomic
    def form_valid(self, form):
        return super().form_valid(form)

class AjaxResponseMixin:
    """Adiciona suporte a respostas AJAX"""
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'status': 'success',
                'message': _('Opération réussie'),
                'redirect_url': self.get_success_url()
            }
            return JsonResponse(data)
        return response

class VerifiedEmailRequiredMixin(LoginRequiredMixin):
    """Garante que o email do usuário está verificado"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified:
            messages.warning(
                request,
                _('Veuillez vérifier votre email avant de continuer.')
            )
            return redirect('verify-email')
        return super().dispatch(request, *args, **kwargs)

class SuperUserRequiredMixin(UserPassesTestMixin):
    """Garante que apenas superusuários podem acessar"""
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Seuls les administrateurs peuvent accéder à cette page.")
        )
        return redirect('home')

class LanguagePreferenceMixin:
    """Adiciona preferência de idioma ao contexto"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = self.request.LANGUAGE_CODE
        return context

class LoggedInRedirectMixin:
    """Redireciona usuários logados"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

class TimezoneContextMixin:
    """Adiciona informações de fuso horário ao contexto"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_timezone'] = timezone.get_current_timezone_name()
        return context

class CacheControlMixin:
    """Controla o cache das views"""
    cache_timeout = 60 * 15  # 15 minutos

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        patch_cache_control = getattr(response, 'patch_cache_control', None)
        if patch_cache_control is not None:
            patch_cache_control(max_age=self.cache_timeout)
        return response

class FormMessageMixin:
    """Adiciona mensagens de sucesso/erro aos formulários"""
    success_message = _("Opération réussie!")
    error_message = _("Une erreur s'est produite. Veuillez réessayer.")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

class OwnershipRequiredMixin(UserPassesTestMixin):
    """Verifica se o usuário é dono do objeto"""
    owner_field = 'user'  # Campo que define o dono do objeto

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.owner_field) == self.request.user

class ActivityTrackingMixin:
    """Rastreia atividade do usuário"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])
        return super().dispatch(request, *args, **kwargs)