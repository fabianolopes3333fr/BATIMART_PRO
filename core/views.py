from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    team_members = [
        {'name': 'Jean Dupont', 'role': 'Fondateur & PDG', 'image': 'team-member-1.jpg'},
        {'name': 'Marie Martin', 'role': 'Directrice des Opérations', 'image': 'team-member-2.jpg'},
        {'name': 'Pierre Lefebvre', 'role': 'Chef de Projet Senior', 'image': 'team-member-3.jpg'},
    ]
    return render(request, 'core/about.html', {'team_members': team_members})

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def projects(request):
    return render(request, 'core/projects.html')

def testimonials(request):
    return render(request, 'core/testimonials.html')

