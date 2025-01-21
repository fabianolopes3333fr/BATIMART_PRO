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

class ClientProfileDetailView(LoginRequiredMixin, DetailView):
    model = ClientProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(ClientProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.filter(
            profile=self.object
        ).order_by('-date_commande')[:5]
        context['quotes'] = Quote.objects.filter(
            profile=self.object
        ).order_by('-date_creation')[:5]
        context['wishlists'] = Wishlist.objects.filter(
            profile=self.object
        ).order_by('-date_creation')
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
        ).order_by('-date_commande')

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
        ).order_by('-date_creation')

class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'profiles/quote_form.html'
    success_url = reverse_lazy('quote-list')

    def form_valid(self, form):
        form.instance.profile = self.request.user.client_profile
        messages.success(
            self.request,
            _('Votre devis a été créé avec succès.')
        )
        return super().form_valid(form)

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'profiles/wishlist_list.html'
    context_object_name = 'wishlists'

    def get_queryset(self):
        return Wishlist.objects.filter(
            profile__user=self.request.user
        ).order_by('-date_creation')

class WishlistCreateView(LoginRequiredMixin, CreateView):
    model = Wishlist
    form_class = WishlistForm
    template_name = 'profiles/wishlist_form.html'
    success_url = reverse_lazy('wishlist-list')

    def form_valid(self, form):
        form.instance.profile = self.request.user.client_profile
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