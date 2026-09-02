import os
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mechanics.models import Mechanic, ServiceRequest
from service_platform.settings import get_allowed_hosts, get_csrf_trusted_origins


class MechanicAPITests(APITestCase):
    def setUp(self):
        self.mechanic = Mechanic.objects.create(
            name='Amit Kumar',
            phone='+919876543210',
            location='Bengaluru',
            rating=4.8,
            is_open=True,
            services=['oil change', 'brake service'],
        )

    def test_list_mechanics(self):
        response = self.client.get(reverse('mechanic-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_create_mechanic_valid_data(self):
        payload = {
            'name': 'Ravi Singh',
            'phone': '+919999999999',
            'location': 'Hyderabad',
            'rating': 4.6,
            'is_open': True,
            'services': ['battery check', 'engine repair'],
        }
        response = self.client.post(reverse('mechanic-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Ravi Singh')

    def test_create_mechanic_with_invalid_phone(self):
        payload = {
            'name': 'Invalid Phone',
            'phone': '12345',
            'location': 'Delhi',
            'rating': 3.5,
            'is_open': True,
            'services': ['tire repair'],
        }
        response = self.client.post(reverse('mechanic-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.data)

    def test_create_service_request_success(self):
        payload = {
            'customer_name': 'Neha Sharma',
            'customer_phone': '+919900001122',
            'vehicle_number': 'MH12AB1234',
            'mechanic_id': self.mechanic.id,
            'service': 'oil change',
            'problem_description': 'Engine makes noisy sound.',
        }
        response = self.client.post(reverse('service-request-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING')
        self.assertEqual(ServiceRequest.objects.count(), 1)

    def test_create_service_request_invalid_service_fails(self):
        payload = {
            'customer_name': 'Suman',
            'customer_phone': '+919800000011',
            'vehicle_number': 'KA01CD4321',
            'mechanic_id': self.mechanic.id,
            'service': 'electric welding',
            'problem_description': 'Vehicle is not starting.',
        }
        response = self.client.post(reverse('service-request-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service', response.data)

    def test_create_service_request_invalid_mechanic_fails(self):
        payload = {
            'customer_name': 'Suman',
            'customer_phone': '+919800000011',
            'vehicle_number': 'KA01CD4321',
            'mechanic_id': 9999,
            'service': 'oil change',
            'problem_description': 'Vehicle is not starting.',
        }
        response = self.client.post(reverse('service-request-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mechanic_id', response.data)

    @patch.dict(os.environ, {'DEBUG': '0', 'RENDER_EXTERNAL_HOSTNAME': 'mini-mechanic-service-api.onrender.com'}, clear=False)
    def test_render_hostname_is_in_allowed_hosts(self):
        self.assertIn('mini-mechanic-service-api.onrender.com', get_allowed_hosts())

    @patch.dict(os.environ, {'DEBUG': '0', 'RENDER_EXTERNAL_HOSTNAME': 'mini-mechanic-service-api.onrender.com'}, clear=False)
    def test_render_hostname_is_in_csrf_trusted_origins(self):
        self.assertIn('https://mini-mechanic-service-api.onrender.com', get_csrf_trusted_origins())
