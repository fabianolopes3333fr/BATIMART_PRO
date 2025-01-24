# accounts/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from . import views
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('change-password/', change_password, name='change_password'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('users/', AdminUserListView.as_view(), name='user_list'),

    # Autenticação
    path(_('connexion/'), auth_views.LoginView.as_view(template_name='accounts/login.html',redirect_authenticated_user=True), name='login'),
    path(_('deconnexion/'), auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    # Registro e Verificação
    path(_('inscription/'), views.SignUpView.as_view(), name='signup'),
    path(_('verification/<str:token>/'), views.verify_email, name='verify-email'),
    path(_('verification-requise/'),views.verification_required,name='verification-required'),
    # Gerenciamento de Senha
    path(_('mot-de-passe/'), include([path(_('modifier/'),views.change_password,name='change-password'),
        path(_('reinitialiser/'),auth_views.PasswordResetView.as_view(
                template_name='accounts/password_reset.html',
                email_template_name='accounts/email/password_reset_email.html',
                subject_template_name='accounts/email/password_reset_subject.txt'
            ),
            name='password-reset'
        ),
        path(_('reinitialiser/<uidb64>/<token>/'),auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html'
            ),name='password-reset-confirm'),
        path(_('reinitialiser/termine/'),auth_views.PasswordResetCompleteView.as_view(
                template_name='accounts/password_reset_complete.html'
            ),name='password-reset-complete'),])),
    
    # Perfil de Usuário
    path(_('profil/'), include([
        path('', views.UserDetailView.as_view(), name='profile'),
        path(_('modifier/'),views.ProfileUpdateView.as_view(),name='profile-update'),
    ])),
    
    # Administração de Usuários (staff only)
    path(_('utilisateurs/'), include([
        path('', views.AdminUserListView.as_view(), name='user-list'),
        path('<int:pk>/',views.AdminUserDetailView.as_view(),name='user-detail'),
        path(_('desactiver/<int:pk>/'),views.deactivate_user,name='deactivate-user'),
    ])),
]