from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse e-mail doit être définie"))
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Adresse e-mail invalide"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        logger.info(f"Utilisateur créé avec l'e-mail : {email}")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

    def get_active_users(self):
        return self.filter(is_active=True)

    def get_inactive_users(self):
        return self.filter(is_active=False)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('adresse e-mail'), unique=True)
    prenom = models.CharField(_('prénom'), max_length=100)
    nom = models.CharField(_('nom'), max_length=100)
    is_staff = models.BooleanField(_('statut staff'), default=False)
    is_active = models.BooleanField(_('actif'), default=True)
    date_inscription = models.DateTimeField(_('date d\'inscription'), auto_now_add=True)

    # Nouveaux champs pour la nationalisation française
    numero_securite_sociale = models.CharField(
        _('numéro de sécurité sociale'),
        max_length=15,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{13}$|^\d{15}$',
            message=_("Le numéro de sécurité sociale doit contenir 13 ou 15 chiffres.")
        )],
        blank=True,
        null=True
    )
    
    adresse = models.CharField(_('adresse'), max_length=255, blank=True)
    code_postal = models.CharField(_('code postal'), max_length=5, blank=True)
    ville = models.CharField(_('ville'), max_length=100, blank=True)
    
    telephone = models.CharField(
        _('téléphone'),
        max_length=10,
        validators=[RegexValidator(
            regex=r'^0\d{9}$',
            message=_("Le numéro de téléphone doit être au format 0XXXXXXXXX.")
        )],
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Normaliser l'email en minuscules
        super().save(*args, **kwargs)