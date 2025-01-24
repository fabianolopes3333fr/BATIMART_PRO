# accounts/views.py
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from .decorators import email_verification_required, grupo_colaborador_required
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import  UserRegistrationForm, UserProfileUpdateForm,ChangePasswordForm, UserForm
from .forms import UserRegistrationForm, UserProfileUpdateForm, ChangePasswordForm, UserForm
from client_profiles.forms import ClientProfileForm
from client_profiles.models import ClientProfile
from company_staff.forms import CompanyStaffProfileForm
from company_staff.models import CompanyStaffProfile
from internal_staff.forms import InternalStaffProfileForm
from internal_staff.models import InternalStaffProfile
# from perfil.forms import PerfilForm
# from perfil.models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, 
from config.mixins import ConfigStaffRequiredMixin, ConfigSuperUserRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse, HttpRequest
from django.utils import timezone
from django.views import View
from .models import User
from typing import Any


class CustomLoginView(LoginView, View):
    template_name = 'login.html'  # Ajuste para o caminho correto do seu template

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.GET.get('session_expired'):
            messages.info(request, _("Votre session a expiré. Veuillez vous reconnecter."))
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.session['last_activity'] = timezone.now().isoformat()
        return response
    
    def check_user_activity(self, request: HttpRequest):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (timezone.now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return JsonResponse({'status': 'logout'})
            
            request.session['last_activity'] = timezone.now().isoformat()
        return JsonResponse({'status': 'active'})

    def logout_view(self, request: HttpRequest, *args: Any, **kwargs: Any):
        logout(request)
        messages.success(request, _("Vous avez été déconnecté avec succès."))
        return redirect('login')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.path.endswith('/logout/'):
            return self.logout_view(request, *args, **kwargs)
        elif request.path.endswith('/check-activity/'):
            return self.check_user_activity(request)
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = UserForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.is_active = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)

            Perfil.objects.create(usuario=usuario)

            send_mail(
                _('Inscription à la plateforme'),
                _("Bonjour, {}, Vous recevrez bientôt un email de autorisation d'utiliser la plateforme.").format(usuario.first_name),
                settings.DEFAULT_FROM_EMAIL,
                [usuario.email],
                fail_silently=False,
            )

            messages.success(request, _("Inscrit. Un email a été envoyé pour que l'administrateur approuve. Attendre le contact"))
            return redirect('login')
        else:
            self.add_form_errors_to_messages(request, form)
        
        return render(request, self.template_name, {"form": form})

    def add_form_errors_to_messages(self, request, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")


@method_decorator(login_required, name='dispatch')
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Votre profil a été mis à jour avec succès!')
        return super().form_valid(form)

    def form_invalid(self, form):
        self.add_form_errors_to_messages(form)
        return super().form_invalid(form)

    def add_form_errors_to_messages(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
    
@method_decorator(grupo_colaborador_required(['administrador', 'colaborador']), name='dispatch')
class AdminUserUpdateView(UserUpdateView):
    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def form_valid(self, form):
        user = form.save()
        if user.is_active:
            send_mail(
                'Inscription approuvée',
                f'Olá, {user.first_name}, votre email a été approuvé sur la plateforme.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        messages.success(self.request, f"L'utilisateur {user.email} a été mis à jour avec succès!")
        return redirect('lista_usuarios')

@method_decorator(grupo_colaborador_required(['administrador', 'colaborador']), name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'lista-usuarios.html'
    context_object_name = 'page_obj'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.select_related('perfil').filter(is_superuser=False)

@method_decorator(grupo_colaborador_required(['administrador', 'colaborador']), name='dispatch')
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'adicionar-usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['perfil_form'] = PerfilForm(self.request.POST, self.request.FILES, user=self.request.user)
        else:
            context['perfil_form'] = PerfilForm(user=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        perfil_form = context['perfil_form']
        if perfil_form.is_valid():
            user = form.save()
            group = Group.objects.get(name='usuario')
            user.groups.add(group)
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            messages.success(self.request, 'Utilisateur ajouté avec succès.')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        perfil_form = context['perfil_form']
        self.add_form_errors_to_messages(form)
        self.add_form_errors_to_messages(perfil_form)
        return super().form_invalid(form)

    def add_form_errors_to_messages(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")






# class UserCreateView(CreateView):
#     model = User
#     form_class = UserForm
#     template_name = 'user_form.html'
#     success_url = '/success/'  # Defina a URL de sucesso apropriada

# class UserUpdateView(UpdateView):
#     model = User
#     form_class = UserForm
#     template_name = 'user_form.html'
#     success_url = '/success/'  # Defina a URL de sucesso apropriada

# class SignUpView(CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'accounts/signup.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(
#             self.request,
#             _('Votre compte a été créé avec succès. Veuillez vérifier votre e-mail.')
#         )
#         user = form.save()
#         user.send_verification_email()
#         return response

# @method_decorator(login_required, name='dispatch')
# class ProfileUpdateView(UpdateView):
#     model = User
#     form_class = UserProfileUpdateForm
#     template_name = 'accounts/profile_update.html'
#     success_url = reverse_lazy('profile')

#     def get_object(self):
#         return self.request.user

#     def form_valid(self, form):
#         messages.success(
#             self.request,
#             _('Votre profil a été mis à jour avec succès.')
#         )
#         return super().form_valid(form)

# @method_decorator([login_required, email_verification_required], name='dispatch')
# class UserDetailView(DetailView):
#     model = User
#     template_name = 'accounts/user_detail.html'
#     context_object_name = 'user'

#     def get_object(self):
#         return self.request.user

# class AdminUserListView(ConfigSuperUserRequiredMixin, ListView):
#     model = User
#     template_name = 'accounts/user_list.html'
#     context_object_name = 'users'
#     paginate_by = 20

#     def dispatch(self, request, *args, **kwargs):
#         self.request = request
#         return super().dispatch(request, *args, **kwargs)  

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = ChangePasswordForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, _('Votre mot de passe a été modifié avec succès.'))
#             return redirect('profile')
#     else:
#         form = ChangePasswordForm(user=request.user)
#     return render(request, 'accounts/change_password.html', {'form': form})

# @login_required
# def verify_email(request, token):
#     try:
#         user = User.objects.get(verification_token=token)
#         user.is_verified = True
#         user.save()
#         messages.success(
#             request,
#             _('Votre e-mail a été vérifié avec succès.')
#         )
#     except User.DoesNotExist:
#         messages.error(
#             request,
#             _('Le lien de vérification est invalide ou a expiré.')
#         )
    
#     return redirect('profile')