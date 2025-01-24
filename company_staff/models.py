from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CompanyStaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_staff_profile')
    company = models.ForeignKey('client_profiles.ClientProfile', on_delete=models.CASCADE, related_name='staff')
    position = models.CharField(_('Position'), max_length=100)
    role = models.CharField(_('Rôle'), max_length=20)
    # ... outros campos do CompanyStaffProfile

    class Meta:
        verbose_name = _('Profil collaborateur entreprise')
        verbose_name_plural = _('Profils collaborateurs entreprise')

    def __str__(self):
        return f"{self.user.email} - {self.company.company_name}"
