from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def services(request):
    return render(request, 'core/services.html')

def projects(request):
    return render(request, 'core/projects.html')

def testimonials(request):
    return render(request, 'core/testimonials.html')

