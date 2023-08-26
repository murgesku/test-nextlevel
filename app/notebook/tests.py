from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact


class ContactCreateTest(APITestCase):
    def test_create_contact(self):
        url = reverse('notebook:contact-list')
        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'phone_number': '+74951234567',
            'email': 'test@example.com'
        }
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contact = Contact.objects.get(pk=response.data['id'])
        self.assertEqual(contact.first_name, 'Иван')
        self.assertEqual(contact.last_name, 'Иванов')
        self.assertEqual(contact.phone_number, '+74951234567')
        self.assertEqual(contact.email, 'test@example.com')

    def test_create_contact_without_email(self):
        url = reverse('notebook:contact-list')
        data = {
            'first_name': 'Пётр',
            'last_name': 'Петров',
            'phone_number': '+74957654321',
            'email': None
        }
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contact = Contact.objects.get(pk=response.data['id'])
        self.assertEqual(contact.first_name, 'Пётр')
        self.assertEqual(contact.last_name, 'Петров')
        self.assertEqual(contact.phone_number, '+74957654321')
        self.assertEqual(contact.email, None)


class ContactRetrieveTest(APITestCase):
    def setUp(self):
        Contact.objects.all().delete()
        contact = Contact(id=1337, first_name='Иван', last_name='Иванов',
                          phone_number='+74951234567', email='test@example.com')
        contact.save()

    def test_contact_retrieve(self):
        url = reverse('notebook:contact-detail', kwargs={'pk': 1337})
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contact = Contact.objects.get(pk=1337)
        self.assertEqual(contact.first_name, 'Иван')
        self.assertEqual(contact.last_name, 'Иванов')
        self.assertEqual(contact.phone_number, '+74951234567')
        self.assertEqual(contact.email, 'test@example.com')

    def test_contact_retrive_invalid(self):
        url = reverse('notebook:contact-detail', kwargs={'pk': 1213})
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactListTest(APITestCase):
    def setUp(self):
        Contact.objects.all().delete()
        Contact.objects.bulk_create(
            [Contact(first_name=f'Имя{i}', last_name=f'Фамилия{i}', phone_number=f'+7000111111{i}') for i in range(20)]
        )

    def test_contact_list(self):
        url = reverse('notebook:contact-list')
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 20)
        self.assertTrue(response.data['next'].endswith('page=2'))
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 10)


class ContactUpdateTest(APITestCase):
    def setUp(self):
        Contact.objects.all().delete()
        contact = Contact(id=1337, first_name='Иван', last_name='Иванов',
                          phone_number='+74951234567', email='test@example.com')
        contact.save()

    def test_contact_update(self):
        url = reverse('notebook:contact-detail', kwargs={'pk': 1337})
        data = {
            'first_name': 'Пётр',
            'last_name': 'Петров',
            'phone_number': '+74957654321',
            'email': None
        }
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contact = Contact.objects.get(pk=1337)
        self.assertEqual(contact.first_name, 'Пётр')
        self.assertEqual(contact.last_name, 'Петров')
        self.assertEqual(contact.phone_number, '+74957654321')
        self.assertEqual(contact.email, None)

    def test_contact_partial_update(self):
        url = reverse('notebook:contact-detail', kwargs={'pk': 1337})
        data = {'email': 'new_test@example.net'}
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contact = Contact.objects.get(pk=1337)
        self.assertEqual(contact.email, 'new_test@example.net')


class ContactDestroyTest(APITestCase):
    def setUp(self):
        Contact.objects.all().delete()
        contact = Contact(id=1337, first_name='Иван', last_name='Иванов',
                          phone_number='+74951234567', email='test@example.com')
        contact.save()

    def test_contact_destroy(self):
        url = reverse('notebook:contact-detail', kwargs={'pk': 1337})
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)


class ContactValidationTest(APITestCase):
    def test_invalid_phone_email(self):
        url = reverse('notebook:contact-list')
        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'phone_number': 'invalid_phone_number',
            'email': 'invalid_email_address'
        }
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 2)

    def test_max_length(self):
        url = reverse('notebook:contact-list')
        data = {
            'first_name': 'ЬЖыРФВвЛлЕХЬасиЪБзХсвПОЛОЗЁЭиъэПЖэЛКюзъдСяыюМгЭБЖеД',
            'last_name': 'ЫнЙБНФшГНЬзУэРдщмаНИЗПяёЩщАзрнЕФАЯэмстнВыЖжЧуккэцзХ',
            'phone_number': '+771555647687382698',
            'email': 'shWAOLJknpHpg1XTi5LkuHbDmKwBpXdG8FyaAtF8HzL2@'
                     'QvGyr86jPOgVzhutZG1QQIp9vienlu27nJYAYeeM95sz7QHJ2WeJ5F0vJ.com'
        }
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 4)
