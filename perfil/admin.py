from django.contrib import admin
from .models import Profile, Purchase, Service, Favorite, Document
from django.utils.translation import gettext_lazy as _

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('user__is_active',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__email', 'product__name')
    date_hierarchy = 'purchase_date'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'service_type')
    search_fields = ('user__email', 'service_type')
    date_hierarchy = 'start_date'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_date')
    list_filter = ('added_date',)
    search_fields = ('user__email', 'product__name')
    date_hierarchy = 'added_date'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'file', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('user__email', 'document_type')
    date_hierarchy = 'uploaded_at'

# Adicione mais classes de admin para outros modelos em perfil, se houver

