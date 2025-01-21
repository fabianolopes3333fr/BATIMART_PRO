from django.contrib import admin
from .models import ClientProfile, Purchase, Quote, Wishlist, Document
from django.utils.translation import gettext_lazy as _

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'full_name', 'email', 'phone_number', 'profession', 'is_active')
    list_filter = ('is_active', 'gender', 'marital_status', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'registration_number', 'profession')
    readonly_fields = ('registration_number', 'created_at', 'updated_at')
    fieldsets = (
        (_('Informations personnelles'), {
            'fields': ('user', 'registration_number', 'birth_date', 'gender', 'marital_status', 'profession')
        }),
        (_('Informations professionnelles'), {
            'fields': ('company', 'company_position', 'professional_email', 'company_phone')
        }),
        (_('Contact d\'urgence'), {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        (_('Adresse de livraison'), {
            'fields': ('delivery_address', 'delivery_number', 'delivery_complement', 'delivery_district', 'delivery_city', 'delivery_state', 'delivery_zip_code', 'delivery_reference')
        }),
        (_('Adresse de facturation'), {
            'fields': ('use_delivery_address', 'billing_address', 'billing_number', 'billing_complement', 'billing_district', 'billing_city', 'billing_state', 'billing_zip_code')
        }),
        (_('Préférences'), {
            'fields': ('language', 'timezone', 'currency')
        }),
        (_('Notifications'), {
            'fields': ('email_notifications', 'sms_notifications', 'whatsapp_notifications', 'newsletter_subscription')
        }),
        (_('Réseaux sociaux'), {
            'fields': ('facebook', 'instagram', 'linkedin', 'twitter')
        }),
        (_('Confidentialité et conditions'), {
            'fields': ('privacy_policy_accepted', 'terms_accepted', 'marketing_consent')
        }),
        (_('Contrôle'), {
            'fields': ('is_active', 'verified_email', 'verified_phone', 'last_login', 'last_order_date', 'created_at', 'updated_at')
        }),
    )

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = _('Nom complet')

    def email(self, obj):
        return obj.user.email
    email.short_description = _('Email')

    def phone_number(self, obj):
        return obj.user.phone
    phone_number.short_description = _('Téléphone')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'profile', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'profile__user__email', 'profile__user__first_name', 'profile__user__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_number', 'profile', 'total_amount', 'status', 'validity_date', 'created_at')
    list_filter = ('status', 'created_at', 'validity_date')
    search_fields = ('quote_number', 'profile__user__email', 'profile__user__first_name', 'profile__user__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('profile__user__email', 'name')
    date_hierarchy = 'created_at'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'type', 'title', 'is_verified', 'uploaded_at')
    list_filter = ('type', 'is_verified', 'uploaded_at')
    search_fields = ('profile__user__email', 'title')
    date_hierarchy = 'uploaded_at'
# Adicione mais classes de admin para outros modelos em perfil, se houver

