from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from functools import wraps

def group_required(group_names):
    """
    Decorator to restrict access to users belonging to specific groups.
    
    Args:
        group_names (str or list): A group name or a list of group names.
    
    Returns:
        function: A decorator that can be used to wrap a view function.
    
    Raises:
        PermissionDenied: If the user doesn't belong to any of the specified groups.
    """
    if isinstance(group_names, str):
        group_names = [group_names]
    
    def check_group(user):
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=group_names).exists()
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not check_group(request.user):
                messages.error(request, _("Vous n'avez pas l'autorisation d'accéder à cette page."))
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    raise PermissionDenied(_("Accès refusé"))
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    return user_passes_test(check_group)

def staff_required(view_func):
    """
    Decorator to restrict access to staff members only.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, _("Cette page est réservée au personnel administratif."))
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view