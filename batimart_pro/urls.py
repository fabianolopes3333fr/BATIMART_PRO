# config/urls.py (arquivo principal do projeto)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    # URLs que não precisam de tradução
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs com tradução
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('', include('accounts.urls')),
    path(_('configuration/'), include('config.urls', namespace='config')),
    path(_('profil/'), include('profiles.urls', namespace='profiles')),
    prefix_default_language=True
)

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)