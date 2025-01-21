from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator
import uuid
import os

class ClientProfile(models.Model):
    GENDER_CHOICES = [
        ('M', _('Masculin')),
        ('F', _('Féminin')),
        ('O', _('Autre')),
    ]
    
    MARITAL_STATUS = [
        ('single', _('Célibataire')),
        ('married', _('Marié(e)')),
        ('divorced', _('Divorcé(e)')),
        ('widowed', _('Veuf/Veuve')),
    ]

    # Relação com User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )

    # Identificação
    registration_number = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    birth_date = models.DateField(_('Date de naissance'))
    gender = models.CharField(
        _('Genre'), 
        max_length=1, 
        choices=GENDER_CHOICES
    )
    marital_status = models.CharField(
        _('État civil'),
        max_length=10,
        choices=MARITAL_STATUS
    )

    # Profissional
    profession = models.CharField(_('Profession'), max_length=100)
    company = models.CharField(_('Entreprise'), max_length=100, blank=True)
    company_position = models.CharField(_('Poste'), max_length=100, blank=True)
    professional_email = models.EmailField(_('Email professionnel'), blank=True)
    company_phone = models.CharField(
        _('Téléphone professionnel'), 
        max_length=20, 
        blank=True
    )

    # Contatos de Emergência
    emergency_contact_name = models.CharField(
        _('Contact d\'urgence - Nom'),
        max_length=100
    )
    emergency_contact_phone = models.CharField(
        _('Contact d\'urgence - Téléphone'),
        max_length=20
    )
    emergency_contact_relation = models.CharField(
        _('Contact d\'urgence - Relation'),
        max_length=50
    )

    # Endereço de Entrega
    delivery_address = models.CharField(_('Adresse de livraison'), max_length=255)
    delivery_number = models.CharField(_('Numéro'), max_length=10)
    delivery_complement = models.CharField(_('Complément'), max_length=100, blank=True)
    delivery_district = models.CharField(_('Quartier'), max_length=100)
    delivery_city = models.CharField(_('Ville'), max_length=100)
    delivery_state = models.CharField(_('État'), max_length=50)
    delivery_zip_code = models.CharField(_('Code postal'), max_length=10)
    delivery_reference = models.TextField(_('Point de repère'), blank=True)

    # Endereço de Cobrança (se diferente)
    use_delivery_address = models.BooleanField(
        _('Utiliser l\'adresse de livraison'), 
        default=True
    )
    billing_address = models.CharField(
        _('Adresse de facturation'), 
        max_length=255, 
        blank=True
    )
    billing_number = models.CharField(_('Numéro'), max_length=10, blank=True)
    billing_complement = models.CharField(
        _('Complément'), 
        max_length=100, 
        blank=True
    )
    billing_district = models.CharField(
        _('Quartier'), 
        max_length=100, 
        blank=True
    )
    billing_city = models.CharField(_('Ville'), max_length=100, blank=True)
    billing_state = models.CharField(_('État'), max_length=50, blank=True)
    billing_zip_code = models.CharField(
        _('Code postal'), 
        max_length=10, 
        blank=True
    )

    # Preferências
    language = models.CharField(
        _('Langue'),
        max_length=5,
        choices=settings.LANGUAGES,
        default='fr'
    )
    timezone = models.CharField(
        _('Fuseau horaire'),
        max_length=50,
        default='Europe/Paris'
    )
    currency = models.CharField(
        _('Devise'),
        max_length=3,
        default='EUR'
    )

    # Notificações
    email_notifications = models.BooleanField(
        _('Notifications email'), 
        default=True
    )
    sms_notifications = models.BooleanField(
        _('Notifications SMS'), 
        default=False
    )
    whatsapp_notifications = models.BooleanField(
        _('Notifications WhatsApp'), 
        default=False
    )
    newsletter_subscription = models.BooleanField(
        _('Abonnement newsletter'), 
        default=True
    )
    
    # Social Media
    facebook = models.URLField(_('Facebook'), blank=True)
    instagram = models.URLField(_('Instagram'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)

    # Privacidade e Termos
    privacy_policy_accepted = models.BooleanField(
        _('Politique de confidentialité acceptée'),
        default=False
    )
    terms_accepted = models.BooleanField(
        _('Conditions d\'utilisation acceptées'),
        default=False
    )
    marketing_consent = models.BooleanField(
        _('Consentement marketing'),
        default=False
    )

    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    verified_email = models.BooleanField(
        _('Email vérifié'), 
        default=False
    )
    verified_phone = models.BooleanField(
        _('Téléphone vérifié'), 
        default=False
    )
    last_login = models.DateTimeField(
        _('Dernière connexion'), 
        null=True, 
        blank=True
    )
    last_order_date = models.DateTimeField(
        _('Date de dernière commande'), 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = _('Profil client')
        verbose_name_plural = _('Profils clients')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email}"

    def get_full_address(self):
        """Retorna o endereço completo formatado"""
        if self.use_delivery_address:
            return f"{self.delivery_address}, {self.delivery_number}, " \
                   f"{self.delivery_complement}, {self.delivery_district}, " \
                   f"{self.delivery_city} - {self.delivery_state}, " \
                   f"{self.delivery_zip_code}"
        return f"{self.billing_address}, {self.billing_number}, " \
               f"{self.billing_complement}, {self.billing_district}, " \
               f"{self.billing_city} - {self.billing_state}, " \
               f"{self.billing_zip_code}"

    @property
    def age(self):
        """Calcula a idade do cliente"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - \
               ((today.month, today.day) < \
               (self.birth_date.month, self.birth_date.day))

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para validações adicionais"""
        if self.use_delivery_address:
            # Copia endereço de entrega para cobrança
            self.billing_address = self.delivery_address
            self.billing_number = self.delivery_number
            self.billing_complement = self.delivery_complement
            self.billing_district = self.delivery_district
            self.billing_city = self.delivery_city
            self.billing_state = self.delivery_state
            self.billing_zip_code = self.delivery_zip_code
        super().save(*args, **kwargs)