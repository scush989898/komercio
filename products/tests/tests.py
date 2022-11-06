from rest_framework.test import APITestCase
from products.models import Product
from accounts.models import Account
from django.db.utils import IntegrityError


class ProductModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product1_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 12,
        }
        cls.product2_data = {
            "description": "Geladeira xiaomi",
            "price": 2000.80,
            "quantity": 90,
        }
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

    def test_should_create_a_product(self):
        """
        it shoul be able to create a product and associate with a Account instance
        """
        seller = Account.objects.create(**self.seller_data)
        product = Product.objects.create(**self.product1_data, seller=seller)
        self.assertEqual(product.description, self.product1_data["description"])
        self.assertEqual(product.price, self.product1_data["price"])
        self.assertEqual(product.quantity, self.product1_data["quantity"])

    def test_should_not_be_able_to_create_a_product_wrong_keys(self):
        """
        it should raise and error for trying to create a product with wrong keys
        """
        seller = Account.objects.create(**self.seller_data)
        with self.assertRaises(IntegrityError):
            Product.objects.create(**self.missing_keys, seller=seller)

    def test_should_not_be_able_to_create_a_product_without_seller(self):
        """
        it should raise and error for trying to create a product without Account instance
        """
        expected_message = 'null value in column "seller_id" of relation "products_product" violates not-null constraint'
        with self.assertRaisesMessage(
            IntegrityError, expected_message=expected_message
        ):
            Product.objects.create(**self.product1_data)


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.products_url = "/api/products/"
        cls.register_account_url = "/api/accounts/"
        cls.login_account_url = "/api/login/"

        cls.product1_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 12,
        }
        cls.product2_data = {
            "description": "Geladeira xiaomi",
            "price": 2000.80,
            "quantity": 90,
        }
        cls.seller_data = {
            "username": "vendedor",
            "password": "abcd",
            "first_name": "vende",
            "last_name": "dor",
            "is_seller": True,
        }
        cls.seller2_data = {
            "username": "vendedor22",
            "password": "abcd22",
            "first_name": "vende22",
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
        cls.seller_token = ""

        cls.seller2_token = ""

        cls.buyer_token = ""

        cls.missing_keys = {}

        cls.seller_credentials = {}
        cls.seller2_credentials = {}
        cls.buyer_credentials = {}

    def setUp(self) -> None:
        seller = self.client.post(self.register_account_url, self.seller_data).data
        st = self.client.post(self.login_account_url, self.seller_data)
        self.seller_token = st.data["token"]

        seller2 = self.client.post(self.register_account_url, self.seller2_data).data
        st2 = self.client.post(self.login_account_url, self.seller2_data)
        self.seller2_token = st2.data["token"]

        buyer = self.client.post(self.register_account_url, self.buyer_data).data
        bt = self.client.post(self.login_account_url, self.buyer_data)
        self.buyer_token = bt.data["token"]

        self.seller_credentials = {"HTTP_AUTHORIZATION": f"Token {self.seller_token}"}
        self.seller2_credentials = {"HTTP_AUTHORIZATION": f"Token {self.seller2_token}"}
        self.buyer_credentials = {"HTTP_AUTHORIZATION": f"Token {self.buyer_token}"}

    def test_should_raise_error_for_not_sending_token(self):
        """
        it should raise an error for not sending token on request headers
        """
        response = self.client.post(self.products_url, self.product1_data)
        self.assertEqual(401, response.status_code)

    def test_should_be_able_to_list_one_product(self):
        """
        it should be able to list a single product already created
        """

        product = self.client.post(
            self.products_url,
            self.product1_data,
            **self.seller_credentials,
        ).data

        response = self.client.get(self.products_url + product["id"] + "/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["id"], product["id"])
        self.assertEqual(response.data["description"], product["description"])

    def test_should_be_able_to_list_all_products(self):
        """
        it should be able to list all products already registered
        """

        self.client.post(
            self.products_url,
            self.product1_data,
            **self.seller_credentials,
        )
        self.client.post(
            self.products_url,
            self.product2_data,
            **self.seller_credentials,
        )
        response = self.client.get(self.products_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.data["count"])

    def test_buyer_should_not_be_able_to_create_product(self):
        """
        it should not be able to a buyer to create a product
        """
        response = self.client.post(
            self.products_url,
            self.product1_data,
            **self.buyer_credentials,
        )
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_should_not_be_able_create_a_product_wrong_keys(self):
        """
        it should not be able to create a product with wrong keys input
        """
        response = self.client.post(
            self.products_url,
            self.missing_keys,
            **self.seller_credentials,
        )
        self.assertEqual(400, response.status_code)

    def test_seller_should_be_able_to_create_a_product(self):
        """
        it should be able to a seller to create a product
        """

        response = self.client.post(
            self.products_url,
            self.product1_data,
            **self.seller_credentials,
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            self.product1_data["description"], response.data["description"]
        )

    def test_product_owner_should_be_able_to_update(self):
        """
        it should be able to a owner update his own products
        """
        product = self.client.post(
            self.products_url,
            self.product1_data,
            **self.seller_credentials,
        ).data

        patched = {"description": "atualizado com sucesso"}

        response = self.client.patch(
            self.products_url + product["id"] + "/",
            patched,
            **self.seller_credentials,
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data["description"], patched["description"])

    def test_others_sellers_should_not_update(self):
        """
        other sellers cannot update products that are not theirs.
        """
        product = self.client.post(
            self.products_url,
            self.product1_data,
            **self.seller_credentials,
        ).data

        patched = {"description": "atualizado com sucesso"}

        response = self.client.patch(
            self.products_url + product["id"] + "/",
            patched,
            **self.seller2_credentials,
        )
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )
