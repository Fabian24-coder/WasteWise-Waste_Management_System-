from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from rest_framework.test import APITestCase

from rubbish.models import RubbishDetail
from .models import pickup_request

User = get_user_model()


class PickupWorkflowTests(APITestCase):
    def setUp(self):
        self.requestor = User.objects.create_user(
            email="requestor@example.com",
            password="SecurePassword123!",
            first_name="Rita",
            last_name="Resident",
        )
        self.collector = User.objects.create_user(
            email="collector@example.com",
            password="SecurePassword123!",
            role="collector",
        )
        self.other_requestor = User.objects.create_user(
            email="other@example.com",
            password="SecurePassword123!",
        )
        self.waste = RubbishDetail.objects.create(
            category="organic",
            name="Food waste",
            rate=Decimal("4.50"),
            unit="kg",
            distance_rate_per_km=Decimal("2.00"),
        )

    def create_request(self):
        self.client.force_authenticate(self.requestor)
        response = self.client.post(
            reverse("pickups:api_create"),
            {
                "contact_name": "Rita Resident",
                "contact_number": "+15550000000",
                "address": "12 Green Street",
                "collection_date": timezone.localdate().isoformat(),
                "waste_type": self.waste.pk,
                "quantity": "10",
                "distance_km": "5",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        return pickup_request.objects.get(pk=response.data["id"])

    def test_requestor_gets_quote_and_only_sees_own_requests(self):
        pickup = self.create_request()
        self.assertEqual(pickup.request_status, "new")
        self.assertEqual(pickup.total_fee, Decimal("55.00"))
        self.assertEqual(pickup.payment_method, "cash")
        self.assertEqual(pickup.user_id, self.requestor)
        self.waste.rate = Decimal("99.00")
        self.waste.save()
        pickup.refresh_from_db()
        self.assertEqual(pickup.total_fee, Decimal("55.00"))

        other_pickup = pickup_request.objects.create(
            user_id=self.other_requestor,
            request_date=date.today(),
            collection_date=date.today(),
            contact_name="Other",
        )
        response = self.client.get(reverse("pickups:api_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [pickup.pk])
        self.assertNotIn(other_pickup.pk, [item["id"] for item in response.data])

    def test_collector_can_accept_schedule_and_requestor_confirms_payment_and_collection(self):
        pickup = self.create_request()
        self.client.force_authenticate(self.collector)
        response = self.client.post(
            reverse("pickups:api_decision", args=[pickup.pk]),
            {
                "action": "accept",
                "scheduled_collection_at": (
                    timezone.now() + timedelta(minutes=5)
                ).isoformat(),
                "collector_message": "We will arrive at the scheduled time.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["request_status"], "accepted")
        self.assertEqual(response.data["collector_id"], self.collector.pk)

        self.client.force_authenticate(self.requestor)
        browser = Client()
        browser.force_login(self.requestor)
        dashboard = browser.get(reverse("pickups:dashboard"))
        self.assertContains(dashboard, "Confirm cash payment")
        response = self.client.post(
            reverse("pickups:api_payment", args=[pickup.pk]), {}, format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["payment_status"], "paid")
        self.assertIsNotNone(response.data["paid_at"])

        dashboard = browser.get(reverse("pickups:dashboard"))
        self.assertContains(dashboard, "Confirm collection")
        self.assertNotContains(dashboard, "Confirm cash payment")
        response = self.client.post(
            reverse("pickups:api_confirm_collection", args=[pickup.pk]),
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["request_status"], "collected")
        self.assertIsNotNone(response.data["collection_confirmed_at"])

        self.client.force_authenticate(self.collector)
        response = self.client.get(reverse("pickups:api_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["request_status"], "collected")

    def test_collector_must_give_reason_when_declining(self):
        pickup = self.create_request()
        self.client.force_authenticate(self.collector)
        url = reverse("pickups:api_decision", args=[pickup.pk])

        response = self.client.post(url, {"action": "decline"}, format="json")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            url,
            {"action": "decline", "decline_reason": "No equipment available."},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["request_status"], "declined")
        self.assertEqual(response.data["decline_reason"], "No equipment available.")

    def test_requestors_cannot_assign_collectors_or_change_status(self):
        self.client.force_authenticate(self.requestor)
        response = self.client.post(
            reverse("pickups:api_create"),
            {
                "contact_name": "Rita Resident",
                "contact_number": "555",
                "address": "12 Green Street",
                "collection_date": timezone.localdate().isoformat(),
                "waste_type": self.waste.pk,
                "quantity": "1",
                "distance_km": "0",
                "collector_id": self.collector.pk,
                "request_status": "accepted",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["request_status"], "new")
        self.assertIsNone(response.data["collector_id"])

        self.client.force_authenticate(self.other_requestor)
        response = self.client.post(
            reverse("pickups:api_payment", args=[response.data["id"]]),
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_only_requestors_can_create_pickup_requests(self):
        self.client.force_authenticate(self.collector)
        response = self.client.post(reverse("pickups:api_create"), {}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_registration_creates_requestor_account_and_allows_login(self):
        browser = Client()
        response = browser.get(reverse("web_register"))
        self.assertEqual(response.status_code, 200)
        response = browser.post(
            reverse("web_register"),
            {
                "email": "new-requestor@example.com",
                "first_name": "New",
                "last_name": "Requestor",
                "password": "AnotherSecurePassword43!",
                "password_confirmation": "AnotherSecurePassword43!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="new-requestor@example.com")
        self.assertEqual(user.role, "requestor")
        self.assertContains(response, "Pickup requests")

        browser.post(reverse("web_logout"))
        response = browser.post(
            reverse("web_login"),
            {"email": user.email, "password": "AnotherSecurePassword43!"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pickup requests")

    def test_payment_cannot_be_confirmed_before_scheduled_day(self):
        pickup = self.create_request()
        self.client.force_authenticate(self.collector)
        scheduled_tomorrow = timezone.now() + timedelta(days=1)
        response = self.client.post(
            reverse("pickups:api_decision", args=[pickup.pk]),
            {
                "action": "accept",
                "scheduled_collection_at": scheduled_tomorrow.isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.client.force_authenticate(self.requestor)
        response = self.client.post(
            reverse("pickups:api_payment", args=[pickup.pk]), {}, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_web_requestor_and_collector_complete_the_workflow(self):
        browser = Client()
        browser.force_login(self.requestor)
        dashboard = browser.get(reverse("pickups:dashboard"))
        self.assertEqual(dashboard.status_code, 200)
        self.assertContains(dashboard, "Waste management at a glance")
        self.assertContains(dashboard, "stats")
        self.assertNotContains(dashboard, "localStorage")
        self.assertContains(dashboard, "When your collector schedules a pickup for today")

        response = browser.get(reverse("pickups:display_pickup_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CleanCity")

        response = browser.post(
            reverse("pickups:place_pickup_request_views"),
            {
                "contact_name": "Rita Resident",
                "contact_number": "+15550000000",
                "address": "12 Green Street",
                "collection_date": timezone.localdate().isoformat(),
                "waste_type": self.waste.pk,
                "quantity": "10",
                "distance_km": "5",
            },
        )
        self.assertEqual(response.status_code, 302)
        pickup = pickup_request.objects.get(user_id=self.requestor)
        self.assertEqual(pickup.total_fee, Decimal("55.00"))

        browser.force_login(self.collector)
        scheduled_at = timezone.now() + timedelta(minutes=5)
        response = browser.post(
            reverse("pickups:update_pickup_requests", args=[pickup.pk]),
            {
                "action": "accept",
                "scheduled_collection_at": scheduled_at.strftime("%Y-%m-%dT%H:%M"),
                "collector_message": "We will arrive as scheduled.",
            },
        )
        self.assertEqual(response.status_code, 302)

        browser.force_login(self.requestor)
        response = browser.get(reverse("pickups:display_pickup_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We will arrive as scheduled.")
        response = browser.post(reverse("pickups:confirm_payment", args=[pickup.pk]))
        self.assertEqual(response.status_code, 302)
        response = browser.post(reverse("pickups:confirm_collection", args=[pickup.pk]))
        self.assertEqual(response.status_code, 302)
        pickup.refresh_from_db()
        self.assertEqual(pickup.request_status, "collected")
