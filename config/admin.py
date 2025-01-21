from django.contrib import admin
from .models import SiteConfig, Page, Menu, MenuItem, BancoImagens, Redirect
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

@admin.register(SiteConfig)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'default_language', 'support_email', 'gdpr_compliant')
    list_filter = ('default_language', 'gdpr_compliant')
    search_fields = ('site_name', 'support_email')
    fieldsets = (
        (_('General'), {'fields': ('site_name', 'default_language', 'support_email')}),
        (_('Compliance'), {'fields': ('gdpr_compliant',)}),
    )
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    inlines = [MenuItemInline]
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')
    list_filter = ('menu',)
    search_fields = ('title',)



@admin.register(BancoImagens)
class BancoDeImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at', 'image_preview')
    search_fields = ('title',)
    date_hierarchy = 'uploaded_at'

    def image_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.file.url)
    image_preview.short_description = 'Preview'
@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'created_at')
    search_fields = ('old_path', 'new_path')
    date_hierarchy = 'created_at'

# Adicione mais classes de admin para outros modelos em config, se houver
