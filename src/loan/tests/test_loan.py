import os
from pathlib import Path

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    force_authenticate,
)

from config.settings import BASE_DIR

User = get_user_model()

APP_DIR = Path(__file__).parent.parent
FIXTURES = [
    os.path.join(BASE_DIR, fixture)
    for fixture in [
        "./authentication/fixtures/users.json",
        "./authentication/fixtures/attendants.json",
        "./authentication/fixtures/customers.json",
        "./shop/fixtures/shops.json",
        "./product/fixtures/products.json",
        "./loan/fixtures/loans.json",
    ]
]


class TestLoan(APITestCase):
    fixtures = FIXTURES

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email="aaaa@a.com", password="aaaaaaaa", phone_number="+420777888988"
        )
        # self.view = LoanViewSet.as_view()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_unauthenticated_loan(self):
        self.assert_(False, "Not Implemented")

    def test_create_authenticated_loan(self):
        self.assert_(False, "Not Implemented")

    def test_cancel_load_return_product(self):
        self.assert_(False, "Not Implemented")

    def test_loan_one_day_after_date_end(self):
        self.assert_(False, "Not Implemented")

    def test_loan_more_than_one_day_after_date_end(self):
        self.assert_(False, "Not Implemented")

    def test_loan_extend_date(self):
        self.assert_(False, "Not Implemented")

    def test_loan_sell_price_for_each_week(self):
        self.assert_(False, "Not Implemented")

    def test_list(self):
        request = self.factory.get("/loan/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = self.view(request)
        self.assertEqual(response.status, status.HTTP_200_OK)

    def test_create(self):
        response: Response = self.client.post(
            path="/loans/",
            data={
                "user": 1,
                "shop": 1,
                "rate": "5",
                "is_active": True,
                "product": {
                    "is_active": True,
                    "description": "string",
                    "buy_price": 0,
                    "sell_price": 0,
                    "quantity": 0,
                    "date_create": "2022-09-29T23:44:23.686Z",
                    "date_extended_deadline": "2022-09-29T23:44:23.686Z",
                    "date_end": "2022-09-29T23:44:23.686Z",
                },
                "customer": {
                    "id_person_number": "000000/0000",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        self.assert_(False, "Not Implemented")
