# config/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import SiteConfig, Menu, BancoImagens,Page,Redirect
import mimetypes

class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = '__all__'
        widgets = {
            'site_description': forms.Textarea(attrs={'rows': 4}),
            'google_maps': forms.Textarea(attrs={'rows': 3}),
            'privacy_policy': forms.Textarea(attrs={'rows': 10}),
            'terms_of_use': forms.Textarea(attrs={'rows': 10}),
            'cookies_policy': forms.Textarea(attrs={'rows': 5}),
            'smtp_password': forms.PasswordInput(),
        }

    def clean_smtp_port(self):
        port = self.cleaned_data.get('smtp_port')
        if port is not None:
            if port < 1 or port > 65535:
                raise forms.ValidationError(_('Port invalide.'))
        else:
            raise forms.ValidationError(_('Le port SMTP est requis.'))
        return port

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = [
            'name', 'url', 'icon', 'order', 
            'parent', 'active', 'target_blank'
        ]
        widgets = {
            'icon': forms.TextInput(attrs={'class': 'icon-picker'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        if parent and parent.parent:
            raise forms.ValidationError(
                _("Un menu ne peut avoir qu'un seul niveau de sous-menu.")
            )
        return cleaned_data

class BancoImagensForm(forms.ModelForm):
    class Meta:
        model = BancoImagens
        fields = ['title', 'file', 'description', 'alt_text']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Verifica o tamanho do arquivo (5MB máximo)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    _('La taille du fichier ne doit pas dépasser 5MB.')
                )

            # Verifica o tipo do arquivo
            file_type = mimetypes.guess_type(file.name)[0]
            allowed_types = [
                'image/jpeg', 'image/png', 'image/gif',
                'application/pdf', 'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            if file_type not in allowed_types:
                raise forms.ValidationError(
                    _('Type de fichier non autorisé.')
                )

        return file

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = [
            'smtp_host', 'smtp_port', 'smtp_user',
            'smtp_password', 'smtp_tls'
        ]
        widgets = {
            'smtp_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Valida as configurações de SMTP
        if cleaned_data.get('smtp_tls') and cleaned_data.get('smtp_port') != 587:
            self.add_error(
                'smtp_port',
                _('Le port 587 est recommandé pour TLS.')
            )
        return cleaned_data

class SEOSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = [
            'meta_title', 'meta_description',
            'meta_keywords', 'google_analytics'
        ]
        widgets = {
            'meta_description': forms.Textarea(attrs={
                'rows': 3,
                'maxlength': 160
            }),
            'meta_keywords': forms.Textarea(attrs={
                'rows': 2,
                'maxlength': 200
            }),
        }

    def clean_meta_title(self):
        title = self.cleaned_data.get('meta_title')
        if title is not None:
            if len(title) > 60:
                raise forms.ValidationError(
                    _('Le titre meta ne doit pas dépasser 60 caractères.')
                )
        else:
            raise forms.ValidationError(
                _('Le titre meta est requis.')
            )
        return title
    
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content']

class RedirectForm(forms.ModelForm):
    class Meta:
        model = Redirect
        fields = ['old_path', 'new_path']