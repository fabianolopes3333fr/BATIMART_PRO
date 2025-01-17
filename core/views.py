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
    projects_list = [
        {
            'title': 'Rénovation d\'appartement',
            'description': 'Rénovation complète d\'un appartement de 100m² à Paris.',
            'image': 'project-1.jpg',
            'category': 'Rénovation'
        },
        {
            'title': 'Peinture extérieure de villa',
            'description': 'Rafraîchissement de la façade d\'une villa de luxe à Cannes.',
            'image': 'project-2.jpg',
            'category': 'Peinture extérieure'
        },
        {
            'title': 'Construction de maison moderne',
            'description': 'Construction d\'une maison contemporaine de 150m² à Lyon.',
            'image': 'project-3.jpg',
            'category': 'Construction'
        },
        {
            'title': 'Décoration intérieure de bureau',
            'description': 'Relooking complet des bureaux d\'une start-up à Bordeaux.',
            'image': 'project-4.jpg',
            'category': 'Décoration'
        },
        {
            'title': 'Peinture industrielle',
            'description': 'Peinture de grande envergure pour un entrepôt à Marseille.',
            'image': 'project-5.jpg',
            'category': 'Peinture industrielle'
        },
        {
            'title': 'Rénovation de façade historique',
            'description': 'Restauration de la façade d\'un bâtiment historique à Strasbourg.',
            'image': 'project-6.jpg',
            'category': 'Restauration'
        }
    ]
    return render(request, 'core/projects.html', {'projects': projects_list})

def testimonials(request):
    testimonials_list = [
        {
            'name': 'Sophie Dubois',
            'role': 'Propriétaire de maison',
            'content': 'BatiMart Pro a complètement transformé notre maison. Leur équipe est professionnelle et attentive aux détails. Je les recommande vivement !',
            'image': 'testimonial-1.jpg'
        },
        {
            'name': 'Marc Leroy',
            'role': 'Gérant d\'entreprise',
            'content': 'Nous avons fait appel à BatiMart Pro pour la rénovation de nos bureaux. Le résultat est au-delà de nos attentes. Un travail remarquable !',
            'image': 'testimonial-2.jpg'
        },
        {
            'name': 'Émilie Moreau',
            'role': 'Architecte d\'intérieur',
            'content': 'En tant que professionnelle, je suis impressionnée par la qualité du travail de BatiMart Pro. Leur expertise technique est inégalée.',
            'image': 'testimonial-3.jpg'
        },
        {
            'name': 'Thomas Petit',
            'role': 'Promoteur immobilier',
            'content': 'BatiMart Pro est notre partenaire de confiance pour tous nos projets. Leur fiabilité et leur savoir-faire sont des atouts précieux.',
            'image': 'testimonial-4.jpg'
        }
    ]
    return render(request, 'core/testimonials.html', {'testimonials': testimonials_list})

