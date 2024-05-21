import os
import tempfile

from flask import Flask, request, render_template
import requests
from requests import utils

VGS_USERNAME = 'US27PigaLSyK4DzmUmBqrLWx'
VGS_PASSWORD = '00c2d428-7849-4fd2-9c29-5b656cd5c26c'
VGS_URL = 'tntza86paji.sandbox.verygoodproxy.com:8443'
PATH_TO_VGS_CA = 'sanbox.pem'

STRIPE_URL = 'https://api.stripe.com/v1/'
STRIPE_TOKEN = 'sk_test_51Lrs6CK6opjUgeSmFHReX14eBMcbofCJrUOisGTC7ASpkfFMqD' \
               '6Eysbs83qBC12YZErV3nv1Pg4UTy9WRhPRVUpQ00o7cUrV8I'

DEBUG = True

app = Flask(__name__)


# Payment Form
@app.route("/")
def payment_form():
    return render_template('index.html', text="")


# Payment success page
@app.route('/payment-success')
def success_page():
    return render_template('payment-success.html')


# Payment failure page
@app.route('/payment-failure')
def failure_page():
    return render_template('payment-failure.html')


# Launch Server
@app.route('/post', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        if DEBUG:
            print(f'request data:', request.json)

        # Get Card number and Card cvc tokens
        card_number_token = request.json['card_number']
        card_cvc_token = request.json['card_cvc']

        # Execute Create Payment through VGS Outbound Proxy
        payment = create_payment(card_number_token, card_cvc_token)
        if not payment:
            return {"status": "payment failed - payment method"}

        # Execute Payment Intent
        intent = payment_intent(payment['id'])
        if not intent:
            return {"status": "payment failed - payment intent"}

        # Get PI status
        intent_status = intent['charges']['data'][0]['status']
        if DEBUG:
            print(f'payment_intent status:', intent_status)
        return {"status": intent_status}
    else:
        return 'Unsupported HTTP method'


# File Read Function
def read_file(path):
    with open(path, mode='rb') as file:
        return file.read()


# Create Payment Method
def create_payment(card_number_token, card_cvc_token):
    proxy = {'https': f'https://{VGS_USERNAME}:{VGS_PASSWORD}@{VGS_URL}'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {STRIPE_TOKEN}'
    }
    payload = {
        'type': 'card',
        'card[number]': card_number_token,
        'card[cvc]': card_cvc_token,
        'card[exp_month]': '12',
        'card[exp_year]': '2024'
    }
    path_to_lib_ca = utils.DEFAULT_CA_BUNDLE_PATH
    with tempfile.NamedTemporaryFile() as ca_file:
        ca_file.write(read_file(PATH_TO_VGS_CA))
        ca_file.write(str.encode(os.linesep))
        ca_file.write(read_file(path_to_lib_ca))
        read_file(ca_file.name)
        try:
            response = requests.post(
                f'{STRIPE_URL}payment_methods', data=payload, headers=headers, proxies=proxy, verify=ca_file.name
            )
            response.raise_for_status()
            print("create_payment successful")
            if DEBUG:
                print('Response:', response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print('create_payment failed', e)


# Execute Payment Intent
def payment_intent(payment_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {STRIPE_TOKEN}'
    }
    payload = {
        'amount': 599,
        'currency': 'usd',
        'payment_method': payment_id,
        'confirm': 'true',
        'return_url': 'https://example.com/return'
    }

    try:
        response = requests.post(f'{STRIPE_URL}payment_intents', headers=headers, data=payload)
        response.raise_for_status()
        print("payment_intent successful")
        if DEBUG:
            print('Response:', response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print('payment_intent failed', e)


if __name__ == '__main__':
    app.run(debug=DEBUG)