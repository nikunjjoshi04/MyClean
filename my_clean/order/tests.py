from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.shortcuts import render
from . import views

# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/order/home/')
        self.assertEquals(response.status_code, 200, "Done0")

    def test_home_page_content(self):
        response = self.client.get('/home/')
        self.assertEquals(response.status_code, 200, "Done0")



