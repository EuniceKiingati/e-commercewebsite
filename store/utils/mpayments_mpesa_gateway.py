import logging
import time
import math
import base64
from datetime import datetime
from django.http import JsonResponse
import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

from store.models import Order


logging = logging.getLogger("default")


class MpesaGateWay:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None

    def __init__(self):
        self.now = datetime.now()
        self.shortcode = settings.SHORT_CODE
        self.consumer_key = settings.CONSUMER_KEY
        self.consumer_secret = settings.CONSUMER_SECRET
        self.access_token_url = settings.ACCESS_TOKEN_URL

        self.password = self.generate_password()
        self.c2b_callback = settings.CALLBACK_URL
        self.checkout_url = settings.CHECKOUT_URL

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def getAccessToken(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper

    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        self.timestamp = self.now.strftime("%Y%m%d%H%M%S")
        password_str = settings.SHORT_CODE + settings.PASS_KEY + self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refreshToken
    def stk_push_request(self, payload):
        data = payload["data"]
        amount = data["amount"]
        order_id = data["order_id"]
        phone_number = data["phone_number"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.c2b_callback,
            "AccountReference": "Sofa KE",
            "TransactionDesc": "Test",
        }
        print(req_data)

        res = requests.post(
            self.checkout_url, json=req_data, headers=self.headers, timeout=30
        )
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            Order.objects.filter(id=order_id).update(
                transaction_id=res_data["CheckoutRequestID"])
        return res_data

    def check_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            logging.error(f"Error: {e}")
            status = 1
        return status

    def get_order_object(self, data):
        transaction_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        order = Order.objects.get(
            transaction_id=transaction_id
        )

        return order

    def callback_handler(self, data):
        status = self.check_status(data)
        order = self.get_order_object(data)
        if status == 0:
            order.complete = True
            order.save()
        logging.info("Order completed info {}".format(data))
        return JsonResponse('Payment complete', safe=False)
