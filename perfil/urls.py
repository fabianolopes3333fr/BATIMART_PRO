# profiles/urls.py
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'profiles'

urlpatterns = [
    # Perfil do Cliente
    path('', views.ClientProfileDetailView.as_view(), name='profile-detail'),
    path(
        _('modifier/'),
        views.ClientProfileUpdateView.as_view(),
        name='profile-update'
    ),
    
    # Compras
    path(_('achats/'), include([
        path('', views.PurchaseListView.as_view(), name='purchase-list'),
        path(
            '<str:numero_commande>/',
            views.PurchaseDetailView.as_view(),
            name='purchase-detail'
        ),
        path(
            _('facture/<str:numero_commande>/'),
            views.download_invoice,
            name='download-invoice'
        ),
    ])),
    
    # Orçamentos
    path(_('devis/'), include([
        path('', views.QuoteListView.as_view(), name='quote-list'),
        path(
            _('creer/'),
            views.QuoteCreateView.as_view(),
            name='quote-create'
        ),
        path(
            '<str:numero_devis>/',
            views.QuoteDetailView.as_view(),
            name='quote-detail'
        ),
        path(
            _('accepter/<str:numero_devis>/'),
            views.accept_quote,
            name='quote-accept'
        ),
        path(
            _('refuser/<str:numero_devis>/'),
            views.reject_quote,
            name='quote-reject'
        ),
    ])),
    
    # Lista de Desejos
    path(_('liste-souhaits/'), include([
        path('', views.WishlistListView.as_view(), name='wishlist-list'),
        path(
            _('creer/'),
            views.WishlistCreateView.as_view(),
            name='wishlist-create'
        ),
        path(
            '<int:pk>/',
            views.WishlistDetailView.as_view(),
            name='wishlist-detail'
        ),
        path(
            _('supprimer/<int:pk>/'),
            views.WishlistDeleteView.as_view(),
            name='wishlist-delete'
        ),
    ])),
    
    # Preferências de Notificação
    path(
        _('preferences-notifications/'),
        views.NotificationPreferencesView.as_view(),
        name='notification-preferences'
    ),
    
    # Documentos
    path(_('documents/'), include([
        path('', views.DocumentListView.as_view(), name='document-list'),
        path(
            _('telecharger/<int:pk>/'),
            views.download_document,
            name='document-download'
        ),
    ])),
]