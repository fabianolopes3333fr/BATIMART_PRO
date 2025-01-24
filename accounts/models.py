import re
import uuid
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils.translation import activate, gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser

from accounts.services import send_verification_email

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse e-mail est obligatoire'))
        email = self.normalize_email(email)
        if not email:
            raise ValueError(_('L\'adresse e-mail fournie n\'est pas valide'))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
    


class User(AbstractBaseUser, PermissionsMixin):
    # Campos de autenticação extras
    username = models.CharField(max_length=100, unique=True, null=True)
    email = models.EmailField(_('email address'), max_length=225, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(
        _('Nom de l\'entreprise'), max_length=255, blank=True, null=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    # ... resto do modelo ...
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    class CivilityChoices(models.TextChoices):
        MONSIEUR = 'M', _('Monsieur')
        MADAME = 'MME', _('Madame')
        MADEMOISELLE = 'MLLE', _('Mademoiselle')

    class UserTypeChoices(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', _('Particulier')
        COMPANY = 'COMPANY', _('Entreprise')

    class LanguageChoices(models.TextChoices):
        FRENCH = 'fr', _('Français')
        ENGLISH = 'en', _('English')
        SPANISH = 'es', _('Español')
        PORTUGUESE_BR = 'pt-br', _('Português Brasil')
        PORTUGUESE = 'pt', _('Português')
    
    civility = models.CharField(
        _('Civilité'),
        max_length=4,
        choices=CivilityChoices.choices,
        blank=True
    )

    user_type = models.CharField(
        _('Type d\'utilisateur'),
        max_length=10,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.INDIVIDUAL
    )

    language = models.CharField(
        max_length=5,
        choices=LanguageChoices.choices,
        default=LanguageChoices.FRENCH,
        verbose_name=_('Langue préférée')
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyUserManager()
    
    
    def __str__(self):
        return self.email
    
    def is_company(self):
        return self.user_type == 'COMPANY'

    def is_individual(self):
        return self.user_type == 'INDIVIDUAL'

    
    
    def send_verification_email(self):
        send_verification_email(self)
        
    def verify_email(self, token):
        if self.email_verification_token == token:
            self.is_verified = True
            self.email_verification_token = None
            self.save()
            return True
        return False

    def generate_username(self):
        if self.email:
            get_email = self.email.split('@')[0]
            return re.sub(r"[^a-zA-Z0-9]", "_", get_email)
        return None

    def save(self, *args, **kwargs):
        if not self.pk:  # Se é um novo usuário
            if not self.username:
                self.username = self.generate_username()
            
            # Verifica se o username gerado já existe
            if User.objects.filter(username=self.username).exists():
                base_username = self.username
                counter = 1
                while User.objects.filter(username=self.username).exists():
                    self.username = f"{base_username}_{counter}"
                    counter += 1

        # Verifica o tipo de usuário e campos obrigatórios
        if self.user_type == self.UserTypeChoices.COMPANY:
            if not hasattr(self, 'company_name') or not self.company_name:
                raise ValidationError(_('Le nom de l\'entreprise est requis pour les comptes d\'entreprise.'))
        elif self.user_type == self.UserTypeChoices.INDIVIDUAL:
            if not self.first_name or not self.last_name:
                raise ValidationError(_('Le prénom et le nom sont requis pour les comptes individuels.'))

        # Normaliza o email
        self.email = self.email.lower().strip()

        # Verifica se o email já existe
        if not self.pk and User.objects.filter(email=self.email).exists():
            raise ValidationError(_('Un utilisateur avec cet email existe déjà.'))

        super(User, self).save(*args, **kwargs)
    # Documentação
    cpf = models.CharField(
        max_length=14, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='Format: 000.000.000-00'
            )
        ]
    )
    rg = models.CharField(max_length=20, blank=True)
    
    # Contato
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Format: +00999999999'
            )
        ]
    )
    
    # Endereço
    zip_code = models.CharField(max_length=8, blank=True)
    address = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=10, blank=True)
    complement = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    
    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_attempts = models.PositiveIntegerField(default=0)
    
    # Configurações
    terms_accepted = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' or self.email

    def get_absolute_url(self):
        return reverse('accounts:user-detail', kwargs={'pk': self.pk})


    # Métodos específicos
    @property
    def full_address(self):
        # Retorna endereço completo formatado
        address_parts = filter(None, [
            self.address,
            self.number,
            self.complement,
            self.district,
            self.city,
            self.state,
            self.zip_code
        ])
        return ', '.join(address_parts)

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.save(update_fields=['login_attempts'])

    def increment_login_attempts(self):
        self.login_attempts += 1
        self.save(update_fields=['login_attempts'])