# config/urls.py
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'config'

urlpatterns = [
    # Configurações do Site
    path('', views.SiteConfigUpdateView.as_view(), name='site-config'),
    
    # Gestão de Menu
    path(_('menu/'), include([
        path('', views.MenuListView.as_view(), name='menu-list'),
        path(
            _('ajouter/'),
            views.MenuCreateView.as_view(),
            name='menu-create'
        ),
        path(
            _('modifier/<int:pk>/'),
            views.MenuUpdateView.as_view(),
            name='menu-update'
        ),
        path(
            _('supprimer/<int:pk>/'),
            views.MenuDeleteView.as_view(),
            name='menu-delete'
        ),
    ])),
    
    # Biblioteca de Mídia
    path(_('mediatheque/'), include([
        path('', views.MediaLibraryListView.as_view(), name='media-list'),
        path(
            _('ajouter/'),
            views.MediaLibraryCreateView.as_view(),
            name='media-create'
        ),
        path(
            '<int:pk>/',
            views.MediaLibraryDetailView.as_view(),
            name='media-detail'
        ),
        path(
            _('modifier/<int:pk>/'),
            views.MediaLibraryUpdateView.as_view(),
            name='media-update'
        ),
        path(
            _('supprimer/<int:pk>/'),
            views.MediaLibraryDeleteView.as_view(),
            name='media-delete'
        ),
    ])),
    
    # Redirecionamentos
    path(_('redirections/'), include([
        path('', views.RedirectListView.as_view(), name='redirect-list'),
        path(
            _('ajouter/'),
            views.RedirectCreateView.as_view(),
            name='redirect-create'
        ),
        path(
            _('modifier/<int:pk>/'),
            views.RedirectUpdateView.as_view(),
            name='redirect-update'
        ),
    ])),
]