from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Page, Section, Menu, Theme

class CoreViewsTestCase(TestCase):
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

# Adicione mais testes para Menu e Theme se necessário
