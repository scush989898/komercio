from rest_framework.test import APITestCase
from accounts.models import Account
from django.core.exceptions import ValidationError


class AccountModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_data = {
            "username": "vendedor",
            "password": "abcd",
            "first_name": "vende",
            "last_name": "dor",
            "is_seller": True,
        }
        cls.buyer_data = {
            "username": "comprador",
            "password": "abcd",
            "first_name": "compra",
            "last_name": "dor",
            "is_seller": False,
        }
        cls.missing_keys = {}
        cls.some_missing_keys = {
            "username": "comprador",
            "password": "abcd",
        }

    def test_should_be_able_to_create_a_seller(self):
        """
        it shoul be able to create a seller
        """
        seller = Account.objects.create(**self.seller_data)
        self.assertEqual(seller.username, self.seller_data["username"])
        self.assertEqual(seller.is_seller, self.seller_data["is_seller"])
        self.assertEqual(seller.first_name, self.seller_data["first_name"])
        self.assertEqual(seller.last_name, self.seller_data["last_name"])
        self.assertEqual(seller.password, self.seller_data["password"])

    def test_should_be_able_to_create_a_buyer(self):
        """
        it shoul be able to create a buyer
        """
        buyer = Account.objects.create(**self.buyer_data)
        self.assertEqual(buyer.username, self.buyer_data["username"])
        self.assertEqual(buyer.is_seller, self.buyer_data["is_seller"])
        self.assertEqual(buyer.first_name, self.buyer_data["first_name"])
        self.assertEqual(buyer.last_name, self.buyer_data["last_name"])
        self.assertEqual(buyer.password, self.buyer_data["password"])

    def test_should_not_be_able_to_create_an_account_with_wrong_keys(self):
        """
        it should raise and error for trying to create an account of any type
        with wrong/missing keys
        """
        with self.assertRaises(ValidationError):
            Account.objects.create(**self.missing_keys).full_clean()

        with self.assertRaises(ValidationError):
            Account.objects.create(**self.some_missing_keys).full_clean()


class AccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.get_url = "/api/accounts/"
        cls.get_newest_url = "/api/accounts/newest/"
        cls.login_url = "/api/login/"
        cls.update_url = "/api/accounts/"
        cls.seller_data = {
            "username": "vendedor",
            "password": "abcd",
            "first_name": "vende",
            "last_name": "dor",
            "is_seller": True,
        }
        cls.buyer_data = {
            "username": "comprador",
            "password": "abcd",
            "first_name": "compra",
            "last_name": "dor",
            "is_seller": False,
        }
        cls.missing_keys = {}
        cls.updated = {"first_name": "alterado", "last_name": "novamente"}

    def test_can_register_seller_account(self):
        """
        it should be able to create a seller type account
        """
        response = self.client.post(self.register_url, self.seller_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.seller_data["username"], response.data["username"])
        self.assertEqual(self.seller_data["first_name"], response.data["first_name"])
        self.assertEqual(self.seller_data["last_name"], response.data["last_name"])
        self.assertEqual(self.seller_data["is_seller"], response.data["is_seller"])
        self.assertEqual(response.data["is_superuser"], False)

    def test_can_register_buyer_account(self):
        """
        it should be able to create a buyer type account
        """
        response = self.client.post(self.register_url, self.buyer_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.buyer_data["username"], response.data["username"])
        self.assertEqual(self.buyer_data["first_name"], response.data["first_name"])
        self.assertEqual(self.buyer_data["last_name"], response.data["last_name"])
        self.assertEqual(self.buyer_data["is_seller"], response.data["is_seller"])
        self.assertEqual(response.data["is_superuser"], False)

    def test_should_raise_error_for_missing_keys(self):
        """
        it should raise an error for missing keys on body input
        """
        response = self.client.post(self.register_url, self.missing_keys)
        self.assertEqual(400, response.status_code)

    def test_should_raise_error_for_violate_unique_constraint_seller(self):
        """
        it should raise an error to violate unique key constraint for the
        username property.
        """
        self.client.post(self.register_url, self.seller_data)
        duplicate = self.client.post(self.register_url, self.seller_data)
        self.assertEqual(400, duplicate.status_code)

    def test_should_raise_error_for_violate_unique_constraint_buyer(self):
        """
        it should raise an error to violate unique key constraint for the
        username property.
        """
        self.client.post(self.register_url, self.buyer_data)
        duplicate = self.client.post(self.register_url, self.buyer_data)
        self.assertEqual(400, duplicate.status_code)

    def test_should_be_able_to_login_seller(self):
        """
        it should be able to perform login with a seller data account.
        """
        self.client.post(self.register_url, self.seller_data)
        response = self.client.post(self.login_url, self.seller_data)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_login_buyer(self):
        """
        it should be able to perform login with a buyer data account.
        """
        self.client.post(self.register_url, self.buyer_data)
        response = self.client.post(self.login_url, self.buyer_data)
        self.assertEqual(200, response.status_code)

    def test_should_not_be_able_to_login(self):
        """
        it should not be able to perform a login with wrong input data
        """
        self.client.post(self.register_url, self.seller_data)
        response = self.client.post(self.login_url, self.missing_keys)
        self.assertEqual(400, response.status_code)

    def test_should_not_be_able_to_update_other_accounts(self):
        """
        it should not be able to perform an update with another user token
        """
        seller = self.client.post(self.register_url, self.seller_data).data
        st = self.client.post(self.login_url, self.seller_data)
        buyer = self.client.post(self.register_url, self.buyer_data).data
        bt = self.client.post(self.login_url, self.buyer_data)
        buyer_token = bt.data["token"]
        seller_token = st.data["token"]
        patch_url = f'{self.update_url}{seller["id"]}/'
        credentials = {"HTTP_AUTHORIZATION": f"Token {buyer_token}"}
        response = self.client.patch(patch_url, self.updated, **credentials)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_should_be_able_to_update(self):
        """
        it should be able to perform an update
        """
        seller = self.client.post(self.register_url, self.seller_data).data
        st = self.client.post(self.login_url, self.seller_data)
        seller_token = st.data["token"]
        patch_url = f'{self.update_url}{seller["id"]}/'
        credentials = {"HTTP_AUTHORIZATION": f"Token {seller_token}"}
        response = self.client.patch(patch_url, self.updated, **credentials)
        self.assertEqual(200, response.status_code)

    def test_should_not_be_able_to_inactive_account(self):
        """
        it should not be able to inactivate an account without admin permissions
        """

        seller = self.client.post(self.register_url, self.seller_data).data
        st = self.client.post(self.login_url, self.seller_data)
        seller_token = st.data["token"]
        management_url = f'{self.update_url}{seller["id"]}/management/'
        credentials = {"HTTP_AUTHORIZATION": f"Token {seller_token}"}
        response = self.client.patch(
            management_url, {"is_active": False}, **credentials
        )
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_should_be_able_to_list_all_users(self):
        """
        it should be able to list all users already registered
        """

        self.client.post(self.register_url, self.seller_data)
        self.client.post(self.register_url, self.buyer_data)
        response = self.client.get(self.get_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["count"], 2)

    def test_should_be_able_to_list_by_newest_users(self):
        """
        it should be able to list newest registered users by num url param
        """

        self.client.post(self.register_url, self.seller_data)
        self.client.post(self.register_url, self.buyer_data)
        response = self.client.get(self.get_newest_url + "1/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["count"], 1)
        buyer = response.data["results"][0]
        self.assertEqual(self.buyer_data["username"], buyer["username"])
        self.assertEqual(self.buyer_data["first_name"], buyer["first_name"])
        self.assertEqual(self.buyer_data["last_name"], buyer["last_name"])
        self.assertEqual(self.buyer_data["is_seller"], buyer["is_seller"])
        self.assertEqual(buyer["is_superuser"], False)
