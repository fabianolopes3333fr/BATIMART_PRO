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
    services_list = [
        {
            'name': 'Peinture intérieure',
            'description': 'Transformez vos espaces intérieurs avec nos services de peinture professionnels.',
            'icon': 'fas fa-paint-roller'
        },
        {
            'name': 'Peinture extérieure',
            'description': 'Protégez et embellissez l\'extérieur de votre propriété avec notre expertise.',
            'icon': 'fas fa-home'
        },
        {
            'name': 'Rénovation',
            'description': 'Services complets de rénovation pour moderniser votre espace de vie ou de travail.',
            'icon': 'fas fa-hammer'
        },
        {
            'name': 'Construction',
            'description': 'De la conception à la réalisation, nous gérons vos projets de construction.',
            'icon': 'fas fa-hard-hat'
        },
        {
            'name': 'Conseil en décoration',
            'description': 'Obtenez des conseils d\'experts pour créer l\'ambiance parfaite dans votre espace.',
            'icon': 'fas fa-swatchbook'
        },
        {
            'name': 'Finitions spéciales',
            'description': 'Techniques de finition avancées pour un look unique et personnalisé.',
            'icon': 'fas fa-magic'
        }
    ]
    return render(request, 'core/services.html', {'services': services_list})

def projects(request):
    return render(request, 'core/projects.html')

def testimonials(request):
    return render(request, 'core/testimonials.html')

