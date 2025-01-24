from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='internal_staff_profile')
    department = models.CharField(_('Department'), max_length=100)
    employee_id = models.CharField(_('Employee ID'), max_length=20, unique=True)
    role = models.CharField(_('Rôle'), max_length=20)
    # ... outros campos do StaffProfile

    class Meta:
        verbose_name = _('Profil employé interne')
        verbose_name_plural = _('Profils employés internes')

    def __str__(self):
        return f"{self.user.email} - {self.department}"
