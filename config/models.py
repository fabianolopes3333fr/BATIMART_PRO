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
    default_language = models.CharField(_('Langue par défaut'), max_length=10)
    
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
    gdpr_compliant = models.BooleanField(_('Conforme RGPD'), default=False)
    
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
    location = models.CharField(_('Emplacement'), max_length=100)
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
    

class Redirect(models.Model):
    old_path = models.CharField(_('Ancien chemin'), max_length=200)
    new_path = models.CharField(_('Nouveau chemin'), max_length=200)
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)

class MenuItem(models.Model):
    title = models.CharField(_('Titre'), max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField(_('Ordre'))
    
class BancoImagens(models.Model):
    titulo = models.CharField(_('Titre'), max_length=255)
    imagem = models.ImageField(_('Image'), upload_to='banco_imagens/')
    descricao = models.TextField(_('Description'), blank=True)
    data_upload = models.DateTimeField(_('Date d\'upload'), auto_now_add=True)
    categoria = models.CharField(_('Catégorie'), max_length=100, blank=True)
    tags = models.CharField(_('Tags'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Image de la banque')
        verbose_name_plural = _('Images de la banque')
        ordering = ['-data_upload']

    def __str__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        # Deletar o arquivo de imagem quando o objeto for deletado
        self.imagem.delete(save=False)
        super().delete(*args, **kwargs)
        
class Page(models.Model):
    title = models.CharField(_('Titre'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    content = RichTextField(_('Contenu'))
    meta_description = models.CharField(_('Meta description'), max_length=160, blank=True)
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    published = models.BooleanField(_('Publié'), default=True)
    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Créé par'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='pages_created'
    )
    updated_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Mis à jour par'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='pages_updated'
    )

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/page/{self.slug}/'

# ... (outras classes de modelo existentes)