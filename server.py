import os
import tempfile
import json

from flask import Flask, request, render_template
import requests
from requests import utils

VGS_USERNAME = 'USuVkW3aDtuwUjP8qceWChNk'
VGS_PASSWORD = '8d9dfa49-a27d-4743-8ec8-dae41dc9c55a'
VGS_URL = 'tnt491nnxg5.sandbox.verygoodproxy.com:8443'
PATH_TO_VGS_CA = 'sanbox.pem'

ADYEN_URL = 'https://checkout-test.adyen.com/v69/payments'
ADYEN_TOKEN = 'AQEvhmfxLILLbhVBw0m/n3Q5qf3Vfqx+LJBJV3BY0iz+yBivhNy8xr1xXEUHUerpyiMQwV1bDb7kfNy1WIxI' \
              'IkxgBw==-ANcH4ZSDzkrUIeDd75VCGpsc3qgyBJb6p3erPRRm1Rg=-IY4t>x~L{nqG3nhZ'

DEBUG = True

app = Flask(__name__)


#----------Client -----------
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


#---------Server-----------
# Launch Server
@app.route('/post', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        if DEBUG:
            print(f'request data:', request.json)


        # Get Card Number and Exp dates tokens
        card_holder = request.json['card_holder']
        card_number_token = request.json['card_number']
        card_exp_month = request.json['card_exp'].split(' / ')[0]
        card_exp_year = request.json['card_exp'].split(' / ')[1]


        #Generate Service Account Access Token:
        sa_token = generate_sa_token()

        print(card_holder)
        print(card_number_token)
        print(card_exp_month)
        print(card_exp_year)
        print(sa_token)

        #Enroll Network Token:
        network_token = enroll_network_token(card_number_token, card_exp_month, card_exp_year, sa_token)
        if not network_token:
            return {"status": "payment failed - network token enrollment"}

        #Post Payment to Adyen:
        process_payment = post_to_adyen(card_number_token, card_exp_month, card_exp_year, card_holder)
        if not process_payment:
            return {"status": "payment failed - process payment with Adyen"}

        return {"status": process_payment['resultCode']}
    else:
        return 'Unsupported HTTP method'


#Generate Service Account Access Token
def generate_sa_token():
    url = "https://auth.verygoodsecurity.com/auth/realms/vgs/protocol/openid-connect/token"
    payload = {
        "client_id": 'AC7tw1TUX-NTDemo-IF744',
        "client_secret": '2e4ba720-d176-4252-a8c7-0541628cc49a',
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    sa_token = response.json()["access_token"]
    return sa_token
    


#Enroll card in a Network Token
def enroll_network_token(card_number_token, card_exp_month, card_exp_year, sa_token):
    url = "https://calm.sandbox.verygoodsecurity.app/network-tokens"
    proxy = {'https': f'https://{VGS_USERNAME}:{VGS_PASSWORD}@{VGS_URL}'}
    headers = {
        "Content-Type": "application/json",
        "Calm-Merchant": "MCnGfwfoiZMu8g4PgCnK81WS",
        "Authorization": f"Bearer {sa_token}"
    }
    payload = {
        "pan_alias": card_number_token,
        "exp_month": card_exp_month,
        "exp_year": card_exp_year
    }
    
    return post_request(url, headers, payload, proxy)


# Post Payment to Adyen
def post_to_adyen(card_number_token, card_exp_month, card_exp_year, card_holder):

    url = ADYEN_URL
    proxy = {'https': f'https://{VGS_USERNAME}:{VGS_PASSWORD}@{VGS_URL}'}
    headers = {
        "X-API-key": ADYEN_TOKEN,
        "vgs-network-token": "yes"}

    payload = {
            "amount":{
                "currency": "USD",
                "value": 1000
                },
            "reference": "12345678",
            "paymentMethod":{
                "type": "scheme",
                "number": card_number_token,
                "expiryMonth": card_exp_month,
                "expiryYear": card_exp_year,
                "cvc": "123",
                "holderName": card_holder
            },
            "merchantAccount": "VGSAccount456ECOM"
        }
    
    return post_request(url, headers, payload, proxy)


#Exec Post request
def post_request(url, headers, payload, proxy):
    path_to_lib_ca = utils.DEFAULT_CA_BUNDLE_PATH
    with tempfile.NamedTemporaryFile() as ca_file:
        ca_file.write(read_file(PATH_TO_VGS_CA))
        ca_file.write(str.encode(os.linesep))
        ca_file.write(read_file(path_to_lib_ca))
        read_file(ca_file.name)
        try:

            response = requests.post(url, 
                                    headers = headers, 
                                    json = payload, 
                                    proxies = proxy,
                                    verify=ca_file.name
                                    )
            response.raise_for_status()

            # Prettify and print the response
            parsed_json = json.loads(response.text)
            formatted_json = json.dumps(parsed_json, indent=4)
            print(formatted_json)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print('create_payment failed', e)
            return 


#--------Misc----------
# File Read Function
def read_file(path):
    with open(path, mode='rb') as file:
        return file.read()
#----------------------


if __name__ == '__main__':
    app.run(debug=DEBUG)