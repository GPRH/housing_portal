import json
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.shortcuts import reverse
from apps.users.tests.factories import UserFactory
from django.contrib.auth.models import Group
from django.core import mail
from django.template.loader import render_to_string


class SimpleAOIListAPITest(APITestCase):
    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(reverse('geodata:simple-aoi-list'))
        assert response.status_code == 403

    def test_list_aois_soledad_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:simple-aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 1
        aoi = content[0]
        assert aoi['city'] == 'TestSoledad'

    def test_list_aois_all_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        soledad = Group.objects.get(name='TestSoledadUserGroup')
        cartagena = Group.objects.get(name='TestCartagenaUserGroup')
        user.groups.add(soledad)
        user.groups.add(cartagena)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:simple-aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 2
        aoi1 = content[0]
        assert aoi1['city'] == 'TestCartagena'
        aoi2 = content[1]
        assert aoi2['city'] == 'TestSoledad'

    def test_list_aois_no_perms(self):
        UserFactory.create(
            email='test@test.com', password='secret',
        )
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:simple-aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content) == 0


class AOIListAPITest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',

    ]

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(reverse('geodata:aoi-list'))
        assert response.status_code == 403

    def test_list_aois_all_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        cartagena = Group.objects.get(name='TestCartagenaUserGroup')
        soledad = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(cartagena)
        user.groups.add(soledad)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 2
        assert content['features'][0]['properties']['city'] == 'TestCartagena'
        assert content['features'][1]['properties']['city'] == 'TestSoledad'

    def test_list_aois_soledad_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        soledad = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(soledad)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 1
        assert content['features'][0]['properties']['city'] == 'TestSoledad'

    def test_list_aois_no_perms(self):
        UserFactory.create(
            email='test@test.com', password='secret',
        )
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:aoi-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 0


class SectorListAPITest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(reverse('geodata:sector-list'))
        assert response.status_code == 403

    def test_list_sectors_soledad_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        soledad = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(soledad)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:sector-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 2
        assert content['features'][0]['properties']['city'] == 'TestSoledad'

    def test_list_sectors_no_perms(self):
        UserFactory.create(
            email='test@test.com', password='secret',
        )
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:sector-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 0


class BuildingListAPITest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(reverse('geodata:building-list'))
        assert response.status_code == 403

    def test_list_buildings_soledad_perms(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        soledad = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(soledad)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:building-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 8
        assert content['features'][0]['properties']['city'] == 'TestSoledad'
        assert content['features'][0]['properties']['aoi_name'] == 'La Central'

    def test_list_buildings_no_perms(self):
        UserFactory.create(
            email='test@test.com', password='secret',
        )
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:block-list'))
        assert response.status_code == 200
        content = json.loads(response.content)
        assert len(content['features']) == 0


class SectorStatsAPIViewTest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('geodata:sector-stats')

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(self.endpoint)
        assert response.status_code == 403

    def test_post_with_anonymous_user(self):
        response = self.client.get(self.endpoint, {}, format='json')
        assert response.status_code == 403

    def test_post_with_authorized_user(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            self.endpoint, {'sectorId': 268}, format='json')
        content = json.loads(response.content)
        assert content['buildings']['taxes']['tax_bins'] == [
            0, 17, 64, 256, 325, 370, 672, 7184, 16000
        ]
        assert response.status_code == 200

    def test_post_with_authorized_user_no_buildings(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            self.endpoint, {'sectorId': 269}, format='json')
        assert response.status_code == 200

    def test_post_with_authorized_user_no_taxes(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestCartagenaUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            self.endpoint, {'sectorId': 267}, format='json')
        content = json.loads(response.content)
        assert content['buildings']['taxes']['tax_bins'] == []
        assert response.status_code == 200


class AOIMVTPermissionTest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.endpoint = 'geodata:aoi-mvt'

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(
            reverse(self.endpoint, kwargs={"aoi_id": 75}))
        assert response.status_code == 403

    def test_get_no_content_with_authenticated_user(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        cartagena = Group.objects.get(name='TestCartagenaUserGroup')
        user.groups.add(cartagena)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            '{0}?tile=1/2/3'.format(
                reverse(self.endpoint, kwargs={"aoi_id": 75}))
        )
        assert response.status_code == 204

    def test_get_with_authenticated_user_bad_group(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        cartagena = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(cartagena)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            '{0}?tile=1/2/3'.format(
                reverse(self.endpoint, kwargs={"aoi_id": 75}))
        )
        assert response.status_code == 403


class DroneImageryAPITest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.endpoint = 'geodata:drone-imagery'

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(
            reverse(
                self.endpoint, kwargs={
                    "aoi": 'el-pozon', 'z': 17,
                    'x': 12345, 'y': 678910,
                }
            ))
        assert response.status_code == 403

    def test_get_with_authenticated_user(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        cartagena = Group.objects.get(name='TestCartagenaUserGroup')
        user.groups.add(cartagena)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            reverse(
                self.endpoint, kwargs={
                    "aoi": 'el-pozon', 'z': 17,
                    'x': 12345, 'y': 678910,
                }
            ))
        assert response.status_code == 404

    def test_get_with_authenticated_user_not_authorized(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        cartagena = Group.objects.get(name='TestSoledadUserGroup')
        user.groups.add(cartagena)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(
            reverse(
                self.endpoint, kwargs={
                    "aoi": 'el-pozon', 'z': 17,
                    'x': 12345, 'y': 678910,
                }
            ))
        assert response.status_code == 403


class ContactAPIViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_not_allowed(self):
        response = self.client.get('/api/geodata/contact/')
        assert response.status_code == 405

    def test_contact_with_missing_auth_token(self):
        response = self.client.post('/api/geodata/contact/', {}, format='json')
        assert response.status_code == 403

    def test_contact_validation(self):
        # invalid email
        response = self.client.post(
            '/api/geodata/contact/',
            {'auth_token': 'test_auth_token', 'email': 'blah'},
            format='json'
        )
        assert response.status_code == 400
        assert response.data['email'] == ['Invalid email']

        # mising email
        response = self.client.post(
            '/api/geodata/contact/', {'auth_token': 'test_auth_token'},
            format='json'
        )
        assert response.status_code == 400
        assert response.data['email'] == ['Invalid email']

        # missing name
        response = self.client.post(
            '/api/geodata/contact/',
            {'auth_token': 'test_auth_token', 'email': 'test@test.com'},
            format='json'
        )
        assert response.status_code == 400
        assert response.data['name'] == ['Invalid name']

        # missing message
        response = self.client.post(
            '/api/geodata/contact/',
            {
                'auth_token': 'test_auth_token', 'email': 'test@test.com',
                'name': 'Test User', 'subject': 'Test subject'
            },
            format='json'
        )
        assert response.status_code == 400
        assert response.data['message'] == ['Invalid message']

    def test_valid_contact(self):
        response = self.client.post(
            '/api/geodata/contact/', {
                'auth_token': 'test_auth_token',
                'email': 'test@test.com',
                'name': 'Test User',
                'message': 'Test Message'
            }, format='json'
        )
        assert response.status_code == 200

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.subject == 'GPRH Contact Form Submission'
        assert email.to == ['test1@test.org', 'test2@test.org']
        assert email.body == render_to_string(
            'contact/contact_form_submission.txt',
            {
                'email': 'test@test.com',
                'name': 'Test User', 'subject': 'Test subject',
                'message': 'Test Message'
            }
        )
