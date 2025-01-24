# decorators.py (pode ser colocado em cada app)
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from functools import wraps
from django.conf import settings

def email_verification_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator para verificar se o email do usuário foi verificado
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_verified:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(
                    request,
                    _('Veuillez vérifier votre e-mail avant de continuer.')
                )
                return redirect('verification-required')
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator

def superuser_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator para verificar se o usuário é superusuário
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='admin:login',
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator para verificar se o usuário é staff
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url='admin:login',
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def profile_owner_required(view_func):
    """
    Decorator para verificar se o usuário é dono do perfil
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile_id = kwargs.get('pk') or kwargs.get('profile_id')
        try:
            profile = ClientProfile.objects.get(pk=profile_id)
            if profile.user == request.user:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied(
                _("Vous n'avez pas la permission d'accéder à ce profil.")
            )
        except ClientProfile.DoesNotExist:
            raise Http404(_("Le profil demandé n'existe pas."))
    return _wrapped_view

def grupo_colaborador_required(groups, login_url=None, redirect_field_name='next'):
    """
    Decorator para verificar se o usuário pertence a pelo menos um dos grupos especificados.
    
    :param groups: Lista de nomes de grupos ou uma string com um único nome de grupo.
    :param login_url: URL para redirecionamento em caso de falha na autenticação.
    :param redirect_field_name: Nome do campo de redirecionamento.
    """
    if isinstance(groups, str):
        groups = [groups]
    
    def check_group(user):
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=groups).exists()
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not check_group(request.user):
                if not request.user.is_authenticated:
                    messages.error(request, _("Veuillez vous connecter pour accéder à cette page."))
                    return redirect(login_url or settings.LOGIN_URL)
                else:
                    messages.error(request, _("Vous n'avez pas les permissions nécessaires pour accéder à cette page."))
                    if settings.DEBUG:
                        raise PermissionDenied(_("L'utilisateur n'appartient pas aux groupes requis: {0}").format(', '.join(groups)))
                    return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    return user_passes_test(check_group, login_url=login_url, redirect_field_name=redirect_field_name)

# Alias para compatibilidade com o código existente
group_required = grupo_colaborador_required