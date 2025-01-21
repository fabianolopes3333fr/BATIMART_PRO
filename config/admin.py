from django.contrib import admin
from .models import SiteConfiguration, Page, Menu, MenuItem, Image, Redirect
from django.utils.translation import gettext_lazy as _

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'default_language', 'support_email', 'gdpr_compliant')
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

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')
    list_filter = ('menu',)
    search_fields = ('title',)
    inlines = [MenuItemInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at')
    search_fields = ('title',)
    date_hierarchy = 'uploaded_at'

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'created_at')
    search_fields = ('old_path', 'new_path')
    date_hierarchy = 'created_at'

# Adicione mais classes de admin para outros modelos em config, se houver
