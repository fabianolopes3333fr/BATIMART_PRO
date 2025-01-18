from operator import is_
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Page, Section, Menu, Theme
from core.forms import ContactForm
from django.core.exceptions import ValidationError

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_obj = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            slug='test-company',
            is_active=True,
        )
        try:
            self.page = Page.objects.create(
                client=self.client_obj,
                title='Home',
                slug='home',
                is_active=True,
            
        )
        except ValidationError as e:
            print(f"Erro ao criar a página de serviços: {e}")
        except Exception as e:
            print(f"Erro inesperado ao criar a página de serviços: {e}")

        self.section = Section.objects.create(
            page=self.page,
            title='Welcome',
            content='Welcome to our site',
            section_type='text'
        )
        self.menu = Menu.objects.create(
            client=self.client_obj,
            name='Home',
            url='/'
        )
        self.theme = Theme.objects.create(
            client=self.client_obj,
            name='Default',
            css='body { background-color: #fff; }'
        )
        
        self.services_page = Page.objects.create(
            client=self.client_obj,
            title='Services',
            slug='services',
            is_active=True
        )

    def test_render_page_view(self):
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/page.html')
        self.assertContains(response, 'Welcome to our site')

    def test_render_page_view_with_page_slug(self):
        response = self.client.get(reverse('core:page', kwargs={
            'client_slug': self.client_obj.slug,
            'page_slug': self.page.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/page.html')
        self.assertContains(response, 'Welcome to our site')

    def test_render_page_view_404(self):
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)

    def test_render_page_view_inactive_page(self):
        self.page.is_active = False
        self.page.save()
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 404)
    def test_render_page_view_with_menu_and_theme(self):
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/page.html')
        self.assertIn('menu', response.context)
        self.assertIn('theme', response.context)
        self.assertEqual(response.context['menu'][0].name, 'Home')
        self.assertEqual(response.context['theme'].name, 'Default')

    def test_render_page_view_with_multiple_sections(self):
        Section.objects.create(
            page=self.page,
            title='Second Section',
            content='More content',
            section_type='text'
        )
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to our site')
        self.assertContains(response, 'More content')

        
        
    def test_home_view(self):
        response = self.client.get(reverse('core:home', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_services_view(self):
        response = self.client.get(reverse('core:page', kwargs={
            'client_slug': self.client_obj.slug,
            'page_slug': 'services'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/page.html')

    def test_projects_view(self):
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/projects.html')

    def test_testimonials_view(self):
        response = self.client.get(reverse('core:testimonials'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/testimonials.html')
        
    def test_contact_view_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_view_post_valid(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('core:contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful form submission
        self.assertRedirects(response, reverse('core:contact_success'))

    def test_contact_view_post_invalid(self):
        form_data = {
            'name': '',  # Invalid: empty name
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('core:contact'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_contact_success_view(self):
        response = self.client.get(reverse('core:contact_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact_success.html')
        
    def test_contact_view_post_invalid_email(self):
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',  # Invalid email format
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('core:contact'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_contact_view_post_empty_message(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': ''  # Empty message
        }
        response = self.client.post(reverse('core:contact'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'message', 'This field is required.')

    def test_render_page_view_with_non_existent_page(self):
        response = self.client.get(reverse('core:page', kwargs={
            'client_slug': self.client_obj.slug,
            'page_slug': 'non-existent-page'
        }))
        self.assertEqual(response.status_code, 404)

    def test_render_page_view_with_inactive_client(self):
        self.client_obj.is_active = False
        self.client_obj.save()
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 404)

    def test_render_page_view_ordering_of_sections(self):
        Section.objects.create(
            page=self.page,
            title='Second Section',
            content='More content',
            section_type='text',
            order=2
        )
        response = self.client.get(reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}))
        self.assertEqual(response.status_code, 200)
        sections = response.context['page'].sections.all()
        self.assertEqual(sections[0].title, 'Welcome')
        self.assertEqual(sections[1].title, 'Second Section')

class CoreUrlsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_obj = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        self.page = Page.objects.create(
            client=self.client_obj,
            title='Home',
            slug='home'
        )

    def test_core_urls(self):
        urls = [
            reverse('core:render_page', kwargs={'client_slug': self.client_obj.slug}),
            reverse('core:page', kwargs={'client_slug': self.client_obj.slug, 'page_slug': self.page.slug})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            
    def test_additional_core_urls(self):
        additional_urls = [
            reverse('core:home'),
            reverse('core:services'),
            reverse('core:projects'),
            reverse('core:testimonials'),
        ]
        for url in additional_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

class CoreModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_client_model(self):
        client = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        self.assertEqual(str(client), 'Test Company')
        self.assertEqual(client.slug, 'test-company')

    def test_page_model(self):
        client = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        page = Page.objects.create(
            client=client,
            title='Test Page',
            slug='test-page'
        )
        self.assertEqual(str(page), 'Test Company - Test Page')

    def test_section_model(self):
        client = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        page = Page.objects.create(
            client=client,
            title='Test Page',
            slug='test-page'
        )
        section = Section.objects.create(
            page=page,
            title='Test Section',
            content='Test content',
            section_type='text'
        )
        self.assertEqual(str(section), 'Test Page - Test Section')
        
    def test_menu_model(self):
        client = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        menu = Menu.objects.create(
            client=client,
            name='Home',
            url='/'
        )
        self.assertEqual(str(menu), 'Test Company - Home')

    def test_theme_model(self):
        client = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )
        theme = Theme.objects.create(
            client=client,
            name='Default Theme',
            css='body { background-color: #fff; }'
        )
        self.assertEqual(str(theme), 'Test Company - Default Theme')

class CoreFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_contact_form(self):
        from .forms import ContactForm
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Adicione mais testes de formulários conforme necessário

class CoreIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_obj = Client.objects.create(
            user=self.user,
            company_name='Test Company',
            plan='basic'
        )

    def test_client_page_integration(self):
        page = Page.objects.create(
            client=self.client_obj,
            title='Test Page',
            slug='test-page'
        )
        Section.objects.create(
            page=page,
            title='Test Section',
            content='Test content',
            section_type='text'
        )
        response = self.client.get(reverse('core:page', kwargs={
            'client_slug': self.client_obj.slug,
            'page_slug': page.slug
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Page')
        self.assertContains(response, 'Test content')
# Adicione mais testes para Menu e Theme se necessário
