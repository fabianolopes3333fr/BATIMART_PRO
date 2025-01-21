from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator
import uuid
import os
from datetime import date
from django.core.validators import FileExtensionValidator
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

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
    def clean(self):
        super().clean()
        if self.birth_date:
            age = (date.today() - self.birth_date).days // 365
            if age < 18:
                raise ValidationError(_('Vous devez avoir au moins 18 ans pour vous inscrire.'))

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
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Le numéro de téléphone doit être au format: '+999999999'.")
    )
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    emergency_contact_phone = models.CharField(
        _('Contact d\'urgence - Téléphone'),
        max_length=20
    )
    emergency_contact_relation = models.CharField(
        _('Contact d\'urgence - Relation'),
        max_length=50
    )
    zip_code_validator = RegexValidator(
    regex=r'^\d{5}$',
    message=_('Le code postal doit contenir 5 chiffres.')
    
    )

    # Endereço de Entrega
    delivery_address = models.CharField(_('Adresse de livraison'), max_length=255)
    delivery_number = models.CharField(_('Numéro'), max_length=10)
    delivery_complement = models.CharField(_('Complément'), max_length=100, blank=True)
    delivery_district = models.CharField(_('Quartier'), max_length=100)
    delivery_city = models.CharField(_('Ville'), max_length=100)
    delivery_state = models.CharField(_('État'), max_length=50)
    delivery_zip_code = models.CharField(
    _('Code postal'), 
    max_length=10, 
    validators=[zip_code_validator]
)
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
    # Dentro do profiles/models.py

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('approved', _('Approuvé')),
        ('processing', _('En traitement')),
        ('shipped', _('Expédié')),
        ('delivered', _('Livré')),
        ('cancelled', _('Annulé')),
        ('refunded', _('Remboursé'))
    ]

    profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.PROTECT,
        related_name='purchases'
    )
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(
        _('Montant total'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        _('Statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Documentos
    invoice = models.FileField(
        _('Facture'),
        upload_to='invoices/%Y/%m/',
        null=True,
        blank=True
    )
    
    # Rastreamento
    tracking_code = models.CharField(
        _('Code de suivi'),
        max_length=50,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Achat')
        verbose_name_plural = _('Achats')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Commande {self.order_number}"

class Quote(models.Model):
    STATUS_CHOICES = [
        ('draft', _('Brouillon')),
        ('sent', _('Envoyé')),
        ('negotiating', _('En négociation')),
        ('accepted', _('Accepté')),
        ('rejected', _('Refusé')),
        ('expired', _('Expiré')),
        ('cancelled', _('Annulé')),
    ]

    profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.PROTECT,
        related_name='quotes'
    )
    quote_number = models.CharField(max_length=20, unique=True)
    validity_date = models.DateField(_('Date de validité'))
    total_amount = models.DecimalField(
        _('Montant total'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        _('Statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    description = models.TextField(_('Description'))
    notes = models.TextField(_('Notes'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Devis')
        verbose_name_plural = _('Devis')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['quote_number']),
            models.Index(fields=['status']),
            models.Index(fields=['validity_date']),
        ]

    def __str__(self):
        return f"Devis {self.quote_number}"

    def clean(self):
        super().clean()
        if self.validity_date and self.validity_date <= timezone.now().date():
            raise ValidationError(
                _('La date de validité doit être dans le futur')
            )

class Wishlist(models.Model):
    profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    name = models.CharField(_('Nom'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    is_public = models.BooleanField(_('Public'), default=False)
    
    # Dados de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Liste de souhaits')
        verbose_name_plural = _('Listes de souhaits')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['profile', 'is_active']),
            models.Index(fields=['is_public']),
        ]

    def __str__(self):
        return f"{self.name} - {self.profile.user.get_full_name()}"

    def clean(self):
        # Limita o número de listas de desejos ativas por usuário
        if self.is_active and not self.pk:  # Se for uma nova lista ativa
            active_lists = Wishlist.objects.filter(
                profile=self.profile,
                is_active=True
            ).count()
            if active_lists >= 5:  # Limite de 5 listas ativas
                raise ValidationError(
                    _('Vous ne pouvez pas avoir plus de 5 listes actives.')
                )

# Dentro do profiles/models.py

class Document(models.Model):
    TYPE_CHOICES = [
        ('invoice', _('Facture')),
        ('contract', _('Contrat')),
        ('certificate', _('Certificat')),
        ('receipt', _('Reçu')),
        ('id_card', _('Carte d\'identité')),
        ('passport', _('Passeport')),
        ('proof_address', _('Justificatif de domicile')),
        ('insurance', _('Assurance')),
        ('other', _('Autre')),
    ]
    user = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(ClientProfile,on_delete=models.CASCADE,related_name='documents')
    type = models.CharField(_('Type'), max_length=20,choices=TYPE_CHOICES)
    title = models.CharField(_('Titre'), max_length=200)
    file = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    description = models.TextField(_('Description'), blank=True)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    
    # Validação e expiração
    is_verified = models.BooleanField(_('Vérifié'), default=False)
    verified_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateField(_('Date d\'expiration'), null=True, blank=True)
    
    # Controle
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['expiry_date']),
        ]
    def get_type_display(self) -> str:
        """
        Este método é gerado automaticamente pelo Django.
        Esta definição é apenas para satisfazer o analisador estático.
        """
        return ""
    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.file:
            if isinstance(self.file, UploadedFile):
                if self.file.size > 10 * 1024 * 1024:  # 10 MB
                    raise ValidationError(_('La taille du fichier ne doit pas dépasser 10 MB'))
                
                ext = os.path.splitext(self.file.name)[1].lower()
                allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
                if ext not in allowed_extensions:
                    raise ValidationError(_('Type de fichier non autorisé. Extensions permises: {}').format(', '.join(allowed_extensions)))


    def save(self, *args, **kwargs):
        if not self.pk:  # Se for novo documento
            import mimetypes
            # Define o tipo MIME do arquivo
            mime_type, _ = mimetypes.guess_type(self.file.name)
            self.mime_type = mime_type or 'application/octet-stream'
            # Define o tamanho do arquivo
            self.file_size = self.file.size
            
        super().save(*args, **kwargs)

    def mark_as_verified(self, user):
        from django.utils import timezone
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'verified_by', 'verified_at'])

    def delete(self, *args, **kwargs):
        # Remove o arquivo físico ao deletar o registro
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)