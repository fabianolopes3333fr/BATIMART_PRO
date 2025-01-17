from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_services_view(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/services.html')

    def test_projects_view(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/projects.html')

    def test_testimonials_view(self):
        response = self.client.get(reverse('testimonials'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/testimonials.html')

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_contact_view_post(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após o envio
        self.assertEqual(len(mail.outbox), 1)  # Verifica se um e-mail foi enviado
        self.assertEqual(mail.outbox[0].subject, f'Nouveau message de Test User: Test Subject')

class CoreUrlsTestCase(TestCase):
    def test_core_urls(self):
        urls = ['home', 'about', 'services', 'projects', 'testimonials', 'contact']
        for url_name in urls:
            url = reverse(url_name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

# Se você tiver modelos no aplicativo core, adicione testes para eles aqui
# class CoreModelsTestCase(TestCase):
#     def test_some_model(self):
#         # Teste seus modelos aqui
#         pass

# Se você tiver formulários no aplicativo core, adicione testes para eles aqui
# class CoreFormsTestCase(TestCase):
#     def test_some_form(self):
#         # Teste seus formulários aqui
#         pass
