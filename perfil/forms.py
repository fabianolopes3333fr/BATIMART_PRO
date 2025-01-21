# profiles/forms.py
from django import forms
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import ClientProfile, Purchase, Wishlist, Document, Quote
import re


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        exclude = ['user', 'registration_number', 'created_at', 'updated_at']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_reference': forms.Textarea(attrs={'rows': 3}),
            'company_position': forms.TextInput(attrs={'placeholder': _('Ex: Directeur, Manager...')}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise forms.ValidationError(_('Vous devez avoir au moins 18 ans.'))
        return birth_date

    def clean_professional_email(self):
        email = self.cleaned_data.get('professional_email')
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_('Email professionnel invalide.'))
        return email

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'delivery_address', 'delivery_number',
            'delivery_complement', 'delivery_district',
            'delivery_city', 'delivery_state',
            'delivery_zip_code', 'delivery_reference'
        ]
        widgets = {
            'delivery_reference': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_delivery_zip_code(self):
        zip_code = self.cleaned_data.get('delivery_zip_code')
        if zip_code and not re.match(r'^\d{5}$', zip_code):  # Formato francês
            raise forms.ValidationError(_('Code postal invalide.'))
        return zip_code
    
class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'use_delivery_address', 'billing_address',
            'billing_number', 'billing_complement',
            'billing_district', 'billing_city',
            'billing_state', 'billing_zip_code'
        ]

    def clean(self):
        cleaned_data = super().clean()
        use_delivery = cleaned_data.get('use_delivery_address')
        if not use_delivery:
            required_fields = [
                'billing_address', 'billing_number',
                'billing_district', 'billing_city',
                'billing_state', 'billing_zip_code'
            ]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, _('Ce champ est obligatoire.'))
        return cleaned_data

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'email_notifications', 'sms_notifications',
            'whatsapp_notifications', 'newsletter_subscription'
        ]

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'privacy_policy_accepted', 'terms_accepted',
            'marketing_consent'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('privacy_policy_accepted'):
            raise forms.ValidationError(
                _('Vous devez accepter la politique de confidentialité.')
            )
        if not cleaned_data.get('terms_accepted'):
            raise forms.ValidationError(
                _('Vous devez accepter les conditions d\'utilisation.')
            )
        return cleaned_data

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation'
        ]

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get('emergency_contact_phone')
        if phone and not re.match(r'^\+?[\d\s-]{8,}$', phone):
            raise forms.ValidationError(_('Numéro de téléphone invalide.'))
        return phone

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        exclude = ['profile', 'created_at', 'updated_at']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['type', 'title', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    # type: ignore
    

    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    _('La taille du fichier ne doit pas dépasser 10MB.')
                )
        return file

class ProfessionalInfoForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'profession', 'company', 'company_position',
            'professional_email', 'company_phone'
        ]

    def clean_company_phone(self):
        phone = self.cleaned_data.get('company_phone')
        if phone and not re.match(r'^\+?[\d\s-]{8,}$', phone):
            raise forms.ValidationError(_('Numéro de téléphone invalide.'))
        return phone

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['facebook', 'instagram', 'linkedin', 'twitter']

    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if value and not value.startswith(('http://', 'https://')):
                cleaned_data[field] = f'https://{value}'
        return cleaned_data

class LanguagePreferencesForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['language', 'timezone', 'currency']
        
# profiles/forms.py


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['total_amount', 'status', 'tracking_code', 'invoice']
        widgets = {
            'total_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tracking_code': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def clean_invoice(self):
        invoice = self.cleaned_data.get('invoice')
        if invoice:
            if invoice.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(
                    _('La taille du fichier ne doit pas dépasser 5MB')
                )
            ext = invoice.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError(
                    _('Extensions autorisées: PDF, JPG, JPEG, PNG')
                )
        return invoice

    def clean_tracking_code(self):
        code = self.cleaned_data.get('tracking_code')
        if code:
            if not code.replace('-', '').isalnum():
                raise forms.ValidationError(
                    _('Le code de suivi ne peut contenir que des lettres, chiffres et tirets')
                )
        return code

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            'total_amount', 'validity_date', 'status',
            'description', 'notes'
        ]
        # ... (widgets permanecem os mesmos)

    def clean_validity_date(self):
        validity_date = self.cleaned_data.get('validity_date')
        if validity_date and validity_date <= timezone.now().date():
            raise forms.ValidationError(
                _('La date de validité doit être dans le futur')
            )
        return validity_date

    def clean_total_amount(self):
        amount = self.cleaned_data.get('total_amount')
        if amount and amount <= 0:
            raise forms.ValidationError(
                _('Le montant doit être supérieur à zéro')
            )
        return amount

class NotificationPreferencesForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'email_notifications',
            'sms_notifications',
            'whatsapp_notifications',
            'newsletter_subscription'
        ]
        widgets = {
            'email_notifications': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'sms_notifications': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'whatsapp_notifications': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'newsletter_subscription': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_notifications'].help_text = _(
            'Recevoir les notifications par e-mail'
        )
        self.fields['sms_notifications'].help_text = _(
            'Recevoir les notifications par SMS'
        )
        self.fields['whatsapp_notifications'].help_text = _(
            'Recevoir les notifications par WhatsApp'
        )
        self.fields['newsletter_subscription'].help_text = _(
            'S\'abonner à notre newsletter'
        )