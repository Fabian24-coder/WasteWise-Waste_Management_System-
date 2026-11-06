from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Collector, Zone

User = get_user_model()


class CollectorApiTests(APITestCase):
    def setUp(self):
        self.requestor = User.objects.create_user(
            email="requestor@example.com",
            password="SecurePasswordForApi123!",
        )
        self.collector_user = User.objects.create_user(
            email="collector@example.com",
            password="SecurePasswordForApi123!",
            role="collector",
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="SecurePasswordForApi123!",
        )

    def test_zone_and_collector_reads_require_authentication(self):
        self.assertEqual(self.client.get(reverse("collectors:api_display_zones")).status_code, 401)
        self.assertEqual(self.client.get(reverse("collectors:api_display_collectors")).status_code, 401)

    def test_only_admin_can_manage_zones(self):
        self.client.force_authenticate(self.requestor)
        response = self.client.post(
            reverse("collectors:api_zone_create"),
            {"name": "North", "description": ""},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("collectors:api_zone_create"),
            {"name": "North", "description": ""},
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Zone.objects.get().name, "North")

    def test_collector_profile_requires_collector_role(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("collectors:api_collector_create"),
            {"user": self.requestor.pk, "phone_number": "555-0100"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Collector.objects.exists())

        response = self.client.post(
            reverse("collectors:api_collector_create"),
            {"user": self.collector_user.pk, "phone_number": "555-0100"},
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Collector.objects.get().user, self.collector_user)

# Create your tests here.
