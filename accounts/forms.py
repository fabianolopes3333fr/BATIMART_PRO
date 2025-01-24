# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import User
import random # escolha aleatoria
import string # contem todas as letras do alfabeto, etc.
from django.core.mail import send_mail
import re

class UserForm(forms.ModelForm):
    
    password_1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput) 
    password_2 = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['language', 'country', 'email','first_name', 'last_name',   'cpf', 'password_1', 'password_2']  
        labels = {
            'language': 'Langue', 
            'country': 'Pays',  # tradução para o campo 'Pays'
            'email': 'E-mail', 
            'first_name': 'Prénom', 
            'last_name': 'Nom', 
            'is_active': 'Utilisateur actif?',
            'cpf': 'CPF',
            
        }
        
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['cpf'].required = False
        
        if self.user and self.user.is_authenticated:
            if 'password_1' in self.fields:
                del self.fields['password_1']
            if 'password_2' in self.fields:
                del self.fields['password_2']
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                
                
    def clean_password_1(self):
        password_1 = self.cleaned_data.get('password_1')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})', password_1):
            raise forms.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule et un caractère spécial."
            )
        return password_1
    
    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError(_("Les mots de passe ne sont pas les mêmes!"))
        return password_2


    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        cpf = cleaned_data.get('cpf')

        if country == 'BR' and not cpf:
            self.add_error('cpf', _('CPF is required for Brazilian users.'))

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['language', 'country', 'email','first_name', 'last_name',   'cpf', 'is_active']
        help_texts = {'cpf': _('CPF is required for Brazilian users.'), 'username': None}
        labels = {
            'language': 'Langue', 
            'country': 'Pays',  # tradução para o campo 'Pays'
            'email': 'E-mail', 
            'first_name': 'Prénom',
            'last_name': 'Nom', 
            'is_active': 'Utilisateur actif?',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and not self.user.groups.filter(name__in=['administrador', 'colaborador']).exists():
            if 'is_active' in self.fields:
                del self.fields['is_active']
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
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

class UserProfileUpdateForm(UserCreationForm):
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


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("Les mots de passe ne correspondent pas."))

        return cleaned_data

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