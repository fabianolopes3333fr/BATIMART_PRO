from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'prenom', 'nom', 'is_staff', 'is_active', 'date_inscription', 'session_status')
    list_filter = ('is_staff', 'is_active', 'date_inscription')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('prenom', 'nom', 'numero_securite_sociale')}),
        (_('Coordonnées'), {'fields': ('adresse', 'code_postal', 'ville', 'telephone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Dates importantes'), {'fields': ('last_login', 'date_inscription')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'prenom', 'nom', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'prenom', 'nom', 'numero_securite_sociale')
    ordering = ('email',)
    readonly_fields = ('date_inscription',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def session_status(self, obj):
        if obj.last_login and (timezone.now() - obj.last_login).seconds < 3600:
            return _('Actif')
        return _('Inactif')
    session_status.short_description = _('Statut de la session')

admin.site.register(CustomUser, CustomUserAdmin)