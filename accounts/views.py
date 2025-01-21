# accounts/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import UserRegistrationForm, UserProfileUpdateForm, ChangePasswordForm
from .decorators import email_verification_required

class SignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Votre compte a été créé avec succès. Veuillez vérifier votre e-mail.')
        )
        user = form.save()
        user.send_verification_email()
        return response

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Votre profil a été mis à jour avec succès.')
        )
        return super().form_valid(form)

@method_decorator([login_required, email_verification_required], name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class AdminUserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(
                    request,
                    _('Votre mot de passe a été modifié avec succès.')
                )
                return redirect('login')
            else:
                messages.error(
                    request,
                    _('Le mot de passe actuel est incorrect.')
                )
    else:
        form = ChangePasswordForm()
    
    return render(
        request,
        'accounts/change_password.html',
        {'form': form}
    )

@login_required
def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_verified = True
        user.save()
        messages.success(
            request,
            _('Votre e-mail a été vérifié avec succès.')
        )
    except User.DoesNotExist:
        messages.error(
            request,
            _('Le lien de vérification est invalide ou a expiré.')
        )
    
    return redirect('profile')