# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'password1', 'password2', 'phone', 'cpf', 'rg', 
            'zip_code', 'address', 'number', 'complement',
            'district', 'city', 'state'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Lettres, chiffres et @/./+/-/_ uniquement.')
        self.fields['password1'].help_text = _(
            'Au moins 8 caractères. Ne peut pas être similaire à vos informations personnelles.'
        )
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Cet email est déjà utilisé.'))
        return email

class UserProfileUpdateForm(UserChangeForm):
    password = None  # Remove o campo de senha

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'zip_code', 'address', 'number', 'complement',
            'district', 'city', 'state'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PasswordChangeCustomForm(forms.Form):
    old_password = forms.CharField(
        label=_('Mot de passe actuel'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_('Nouveau mot de passe'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label=_('Confirmer le nouveau mot de passe'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("Les mots de passe ne correspondent pas."))

        return cleaned_data

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email, is_verified=True).exists():
            raise forms.ValidationError(_('Cet email est déjà vérifié.'))
        return email

class ResetPasswordRequestForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Aucun compte trouvé avec cet email.'))
        return email