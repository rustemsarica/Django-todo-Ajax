from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from .forms import NewRecordForm
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

# Create your tests here.


class AjaxFunctions(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('12345')
        self.user.save()

        self.c = Client()
        logged_in = self.c.login(username='test_user', password='12345')

    def test_get_form(self):

        response = self.c.post(reverse('get_form'))
        self.assertEqual(response.status_code, 200)



