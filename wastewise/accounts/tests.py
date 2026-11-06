from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationApiTests(APITestCase):
    def test_registration_always_creates_requestor(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "new@example.com",
                "password": "SecurePasswordForApi123!",
                "first_name": "New",
                "last_name": "User",
                "role": "admin",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        user = User.objects.get(email="new@example.com")
        self.assertEqual(user.role, "requestor")
        self.assertNotIn("password", response.data)

    def test_login_returns_token_and_logout_revokes_it(self):
        user = User.objects.create_user(
            email="api-user@example.com",
            password="SecurePasswordForApi123!",
        )
        response = self.client.post(
            reverse("login"),
            {"email": user.email, "password": "SecurePasswordForApi123!"},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        token = response.data["token"]
        self.assertEqual(response.data["user"]["role"], "requestor")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(reverse("logout"), {}, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, 401)

    def test_me_endpoint_does_not_allow_role_escalation(self):
        user = User.objects.create_user(
            email="requestor@example.com",
            password="SecurePasswordForApi123!",
        )
        self.client.force_authenticate(user)
        response = self.client.patch(
            reverse("me"),
            {"first_name": "Updated", "role": "admin", "is_staff": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200, response.data)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.role, "requestor")
        self.assertFalse(user.is_staff)

# Create your tests here.
