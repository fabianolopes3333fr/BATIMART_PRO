from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django import forms
import csv


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'colored_status')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def colored_status(self, obj):
        if obj.is_active:
            color = 'green'
            status = 'Active'
        else:
            color = 'red'
            status = 'Inactive'
        return format_html('<span style="color: {};">{}</span>', color, status)
    colored_status.short_description = 'Status'

    actions = ['make_active', 'make_inactive', 'export_selected_users']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected users as inactive"

    def export_selected_users(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'First name', 'Last name', 'Is staff', 'Is active'])
        users = queryset.values_list('email', 'first_name', 'last_name', 'is_staff', 'is_active')
        for user in users:
            writer.writerow(user)
        return response
    export_selected_users.short_description = "Export selected users to CSV"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-users/', self.import_users),
        ]
        return my_urls + urls

    def import_users(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    User.objects.create(
                        email=row['email'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        is_staff=row['is_staff'] == 'True',
                        is_active=row['is_active'] == 'True'
                    )
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        else:
            form = CsvImportForm()

        context = {"form": form}
        return render(request, "admin/csv_form.html", context)

# Adicione mais classes de admin para outros modelos em accounts, se houver

