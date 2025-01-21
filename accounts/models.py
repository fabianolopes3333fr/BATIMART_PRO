from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class User(AbstractUser):
    # Campos de autenticação extras
    email = models.EmailField(_('email'), unique=True)
    is_verified = models.BooleanField(default=False)
    
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
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.email

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