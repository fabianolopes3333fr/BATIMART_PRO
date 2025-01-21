from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator
from ckeditor.fields import RichTextField
import mimetypes
import os

class SiteConfig(models.Model):
    # Configurações Básicas
    site_name = models.CharField(_('Nom du site'), max_length=100)
    site_description = RichTextField(_('Description du site'))
    
    # Contato
    contact_email = models.EmailField(_('Email'))
    contact_phone = models.CharField(_('Téléphone'), max_length=20)
    support_hours = models.CharField(_('Heures de support'), max_length=100)
    
    # Endereço
    address = models.TextField(_('Adresse'))
    google_maps = models.TextField(_('Google Maps'), blank=True)
    
    # SEO
    meta_title = models.CharField(_('Meta titre'), max_length=60)
    meta_description = models.CharField(_('Meta description'), max_length=160)
    meta_keywords = models.CharField(_('Meta mots-clés'), max_length=200)
    google_analytics = models.CharField(max_length=50, blank=True)
    
    # LGPD/GDPR
    privacy_policy = RichTextField(_('Politique de confidentialité'))
    terms_of_use = RichTextField(_('Conditions d\'utilisation'))
    cookies_policy = models.TextField(_('Politique des cookies'))
    
    # Email
    smtp_host = models.CharField(max_length=100)
    smtp_port = models.IntegerField(default=587)
    smtp_user = models.CharField(max_length=100)
    smtp_password = models.CharField(max_length=100)
    smtp_tls = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Configuration du site')
        verbose_name_plural = _('Configurations du site')

    def __str__(self):
        return self.site_name

class Menu(models.Model):
    name = models.CharField(_('Nom'), max_length=100)
    url = models.CharField(_('URL'), max_length=200)
    icon = models.CharField(_('Icône'), max_length=50, blank=True)
    order = models.IntegerField(_('Ordre'), default=0)
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Menu parent'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    active = models.BooleanField(_('Actif'), default=True)
    target_blank = models.BooleanField(_('Nouvelle fenêtre'), default=False)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

class MediaLibrary(models.Model):
    title = models.CharField(_('Titre'), max_length=200)
    file = models.FileField(
        _('Fichier'), 
        upload_to='media_library/%Y/%m/'
    )
    description = models.TextField(_('Description'), blank=True)
    alt_text = models.CharField(_('Texte alternatif'), max_length=200)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Médiathèque')
        verbose_name_plural = _('Médiathèque')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and self.file:  # Se for novo arquivo e tiver arquivo
            self.file_size = self.file.size
            file_name = self.file.name
            mime_type, _ = mimetypes.guess_type(file_name)
            self.mime_type = mime_type or 'application/octet-stream'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove o arquivo físico ao deletar o registro
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)