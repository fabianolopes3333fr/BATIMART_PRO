# profiles/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, UpdateView, ListView,
    CreateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import (
    ClientProfile, Purchase, Quote,
    Wishlist
)
from .forms import (
    ClientProfileForm, PurchaseForm,
    QuoteForm, WishlistForm,
    NotificationPreferencesForm
)
from .mixins import ProfileOwnerRequiredMixin

class ProfileDetailView(ProfileOwnerRequiredMixin, DetailView):
    model = ClientProfile  # Corrigido
    template_name = 'profiles/detail.html'
    
    def get_object(self):
        return get_object_or_404(ClientProfile, pk=self.kwargs['pk'])  # Corrigido

class ClientProfileDetailView(LoginRequiredMixin, DetailView):
    model = ClientProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(ClientProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        context['purchases'] = Purchase.objects.filter(
            profile=profile
        ).order_by('-created_at')[:5]  # Alterado de date_commande para created_at
        
        context['quotes'] = Quote.objects.filter(
            profile=profile
        ).order_by('-created_at')[:5]  # Alterado de date_creation para created_at
        
        context['wishlists'] = Wishlist.objects.filter(
            profile=profile
        ).order_by('-created_at')  # Alterado de date_creation para created_at
    
        return context

class ClientProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientProfile
    form_class = ClientProfileForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return get_object_or_404(ClientProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Votre profil a été mis à jour avec succès.')
        )
        return super().form_valid(form)

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'profiles/purchase_list.html'
    context_object_name = 'purchases'
    paginate_by = 10

    def get_queryset(self):
        return Purchase.objects.filter(
            profile__user=self.request.user
        ).order_by('-created_at')  # Alterado de date_commande para created_at

class PurchaseDetailView(ProfileOwnerRequiredMixin, DetailView):
    model = Purchase
    template_name = 'profiles/purchase_detail.html'
    context_object_name = 'purchase'

class QuoteListView(LoginRequiredMixin, ListView):
    model = Quote
    template_name = 'profiles/quote_list.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.filter(
            profile__user=self.request.user
        ).order_by('-created_at')  # Alterado de date_creation para created_at

class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'profiles/quote_form.html'
    success_url = reverse_lazy('quote-list')

    def form_valid(self, form):
        # Busca o perfil do cliente explicitamente
        client_profile = get_object_or_404(
            ClientProfile,
            user=self.request.user
        )
        
        # Define o perfil no formulário
        form.instance.profile = client_profile
        
        messages.success(
            self.request,
            _('Votre devis a été créé avec succès.')
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'status': 'draft'}  # Status inicial como rascunho
        return kwargs

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'profiles/wishlist_list.html'
    context_object_name = 'wishlists'

    def get_queryset(self):
        return Wishlist.objects.filter(
            profile__user=self.request.user
        ).order_by('-created_at')  # Alterado de date_creation para created_at

class WishlistCreateView(LoginRequiredMixin, CreateView):
    model = Wishlist
    form_class = WishlistForm
    template_name = 'profiles/wishlist_form.html'
    success_url = reverse_lazy('wishlist-list')

    def form_valid(self, form):
        # Busca o perfil do cliente de forma explícita
        client_profile = get_object_or_404(
            ClientProfile,
            user=self.request.user
        )
        
        # Associa o perfil à lista de desejos
        form.instance.profile = client_profile
        
        messages.success(
            self.request,
            _('Votre liste de souhaits a été créée.')
        )
        return super().form_valid(form)

class WishlistDeleteView(ProfileOwnerRequiredMixin, DeleteView):
    model = Wishlist
    template_name = 'profiles/wishlist_confirm_delete.html'
    success_url = reverse_lazy('wishlist-list')

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('La liste de souhaits a été supprimée.')
        )
        return super().delete(request, *args, **kwargs)

class NotificationPreferencesView(LoginRequiredMixin, UpdateView):
    model = ClientProfile
    form_class = NotificationPreferencesForm
    template_name = 'profiles/notification_preferences.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return get_object_or_404(ClientProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Vos préférences de notification ont été mises à jour.')
        )
        return super().form_valid(form)
    
