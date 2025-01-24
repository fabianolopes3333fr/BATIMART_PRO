from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
import re

class ClientProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', _('Célibataire')),
        ('married', _('Marié(e)')),
        ('divorced', _('Divorcé(e)')),
        ('widowed', _('Veuf/Veuve')),
    ]
    

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    
    # Informações pessoais
    date_of_birth = models.DateField(_('Date de naissance'), null=True, blank=True)
    phone_number = models.CharField(_('Numéro de téléphone'), max_length=20, blank=True)
    address = models.TextField(_('Adresse'), blank=True)
    city = models.CharField(_('Ville'), max_length=100, blank=True)
    postal_code = models.CharField(_('Code postal'), max_length=10, blank=True)
    country = models.CharField(_('Pays'), max_length=100, blank=True)
    marital_status = models.CharField(_('État civil'), max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True)

    # Informações profissionais
    company_name = models.CharField(_('Nom de l\'entreprise'), max_length=200, blank=True)
    commercial_name = models.CharField(_('Nom commercial'), max_length=255, blank=True, null=True)
    siren = models.CharField(_('SIREN'), max_length=9, blank=True, null=True)
    vat_number = models.CharField(_('TVA Intracommunautaire'), max_length=20, blank=True, null=True)
    billing_address = models.CharField(_('Adresse de facturation'), max_length=255, blank=True, null=True)
    address_complement = models.CharField(_('Complément d\'adresse'), max_length=255, blank=True, null=True)
    billing_country = CountryField(_('Pays de facturation'), blank_label='(select country)', null=True, blank=True)
    job_title = models.CharField(_('Titre du poste'), max_length=100, blank=True)
    company_address = models.TextField(_('Adresse de l\'entreprise'), blank=True)
    company_phone = models.CharField(_('Téléphone professionnel'), max_length=20, blank=True)
    
    class LegalFormChoices(models.TextChoices):
        SARL = 'SARL', _('SARL')
        SAS = 'SAS', _('SAS')
        SA = 'SA', _('SA')
        EI = 'EI', _('Entreprise Individuelle')
        EIRL = 'EIRL', _('EIRL')
        AUTRE = 'AUTRE', _('Autre')

    legal_form = models.CharField(
        _('Forme juridique'),
        max_length=10,
        choices=LegalFormChoices.choices,
        blank=True,
        null=True
    )

    activity_type = models.CharField(_('Type d\'activité'), max_length=255, blank=True, null=True)
    ape_code = models.CharField(_('Code APE'), max_length=5, blank=True, null=True)
    commercial_phone = models.CharField(
        _('Téléphone commercial'),
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Le numéro de téléphone doit être au format: "+999999999". Jusqu\'à 15 chiffres autorisés.')
            )
        ]
    )

    cnpj = models.CharField(
        _('CNPJ'),
        max_length=18,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message=_('CNPJ doit être au format: 00.000.000/0000-00')
            )
        ]
    )

    # ... (métodos existentes) ...

    def clean(self):
        super().clean()
        if self.country == 'BR' and self.user_type == self.UserTypeChoices.COMPANY and not self.cnpj:
            raise ValidationError(_('CNPJ est obligatoire pour les entreprises brésiliennes.'))
        
        if self.cnpj:
            if not self.validate_cnpj(self.cnpj):
                raise ValidationError(_('CNPJ invalide.'))

    @staticmethod
    def validate_cnpj(cnpj):
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        if len(cnpj) != 14:
            return False
        
        if cnpj == cnpj[0] * 14:
            return False

        # Validação dos dígitos verificadores
        total = 0
        factor = 5
        for i in range(12):
            total += int(cnpj[i]) * factor
            factor = 9 if factor == 2 else factor - 1
        
        remainder = total % 11
        check_digit1 = 0 if remainder < 2 else 11 - remainder
        
        if int(cnpj[12]) != check_digit1:
            return False
        
        total = 0
        factor = 6
        for i in range(13):
            total += int(cnpj[i]) * factor
            factor = 9 if factor == 2 else factor - 1
        
        remainder = total % 11
        check_digit2 = 0 if remainder < 2 else 11 - remainder
        
        return int(cnpj[13]) == check_digit2

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # Preferências
    preferred_contact_method = models.CharField(_('Méthode de contact préférée'), max_length=50, blank=True)
    newsletter_subscription = models.BooleanField(_('Abonné à la newsletter'), default=False)

    # Informações do sistema
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    is_verified = models.BooleanField(_('Profil vérifié'), default=False)

    class Meta:
        verbose_name = _('Profil client')
        verbose_name_plural = _('Profils clients')

    def __str__(self):
        return f"Profil de {self.user.get_full_name() or self.user.email}"

    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.postal_code}, {self.country}"

class ClientDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id', _('Pièce d\'identité')),
        ('proof_address', _('Justificatif de domicile')),
        ('other', _('Autre')),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(_('Type de document'), max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(_('Fichier'), upload_to='client_documents/')
    uploaded_at = models.DateTimeField(_('Téléchargé le'), auto_now_add=True)
    is_verified = models.BooleanField(_('Vérifié'), default=False)

    class Meta:
        verbose_name = _('Document client')
        verbose_name_plural = _('Documents clients')
    def get_document_type_display(self) -> str:
        """
        Este método é gerado automaticamente pelo Django.
        Esta definição é apenas para satisfazer o analisador estático.
        """
        return ""

    def __str__(self):
        return f"{self.get_document_type_display()} de {self.client.user.get_full_name()}"