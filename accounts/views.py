from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .forms import EmailAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                return redirect('dashboard')  # Certifique-se de que 'dashboard' é o nome correto da URL
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')  # Substitua 'home' pelo nome da sua URL de página inicial
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Votre compte a été créé avec succès!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Il y a eu une erreur lors de la création de votre compte. Veuillez réessayer.")
        return super().form_invalid(form)


