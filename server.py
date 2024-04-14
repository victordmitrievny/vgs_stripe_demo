from flask import Flask, request, render_template
import requests 
from requests import utils
import tempfile
import os

#------------------------------------Launch server and execute functions-------------------------
app = Flask(__name__)

#Payment Form
@app.route("/")
def payment_form(): 
    return render_template('index.html', text="") 

#Payment success page
@app.route('/payment-success')
def success_page():
    return render_template('payment-success.html')

#Payment failure page
@app.route('/payment-failure')
def failure_page():
    return render_template('payment-failure.html')

#Launch Server
@app.route('/post', methods=['POST'])
def handle_request():
    if request.method == 'POST':

        #Recieve Tokenized Data through VGS Inbound Proxy
        tok_data = request.json
        print('*************')
        print(tok_data)
        print('*************')

        #Get Card number and Card cvc tokens
        card_number_token = tok_data['card_number']
        card_cvc_token = tok_data['card_cvc']

        #Execute Create Payment through VGS Outbound Proxy
        pm_json = create_payment(card_number_token, card_cvc_token)
        if pm_json == None:
            return {"status": "payment failed - payment method"}
        print('*************')

        #Get Payment ID
        payment_id = pm_json['id']
        print('Payment id - ', payment_id)
        print('*************')

        #Execute Payment Intent
        pi_json = payment_intent(payment_id)
        if pi_json == None:
            return {"status": "payment failed - payment intent"}
        print('*************')

        #Get PI status
        pi_status = (pi_json['charges']['data'])[0]['status']
        print(pi_status)
        print('*************')

        return {"status": pi_status}
    
    else:
        return 'Unsupported HTTP method'

#--------------------------------------Functions Definitions---------------------------------------
#Create Payment Method
def create_payment(card_number_token, card_cvc_token):

    #Payment methods
    url = 'https://api.stripe.com/v1/payment_methods'
    username = 'USmWgaETK73AQjt7x6FJPj5f' #Username from VGS account
    password = '61276cc8-5262-4bcc-8ec6-ffce3096228a' #Password from VGS accounts
    proxy = {'https': 'https://' + username + ':' + password + '@tntamsjq33t.sandbox.verygoodproxy.com:8443'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',  
        'Authorization': 'Bearer sk_test_51Lrs6CK6opjUgeSmFHReX14eBMcbofCJrUOisGTC7ASpkfFMqD6Eysbs83qBC12YZErV3nv1Pg4UTy9WRhPRVUpQ00o7cUrV8I' #Stripe AUTH KEY
        }
    payload = {
        'type': 'card',
        'card[number]': card_number_token,
        'card[cvc]': card_cvc_token,
        'card[exp_month]': '12',
        'card[exp_year]': '2024'
    }
    path_to_lib_ca = utils.DEFAULT_CA_BUNDLE_PATH 
    path_to_vgs_ca = '/Users/victordmitirev/Desktop/VGS_demo_app/sanbox.pem' #CA certificate path

    #CA certificate verification
    with tempfile.NamedTemporaryFile() as ca_file:
        ca_file.write(read_file(path_to_vgs_ca))
        ca_file.write(str.encode(os.linesep))
        ca_file.write(read_file(path_to_lib_ca))
        read_file(ca_file.name)

        #POST request
        try:
            response = requests.post(url, data=payload, headers=headers, proxies=proxy, verify=ca_file.name)
            response.raise_for_status()
            print('Create Payment Methos - POST request successful!')
            print('Response:', response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print('POST failed', e)
            print('Response:', response.json())
            return None


#Execute Payment Intent
def payment_intent(payment_id):

    #Payment Intent
    url = 'https://api.stripe.com/v1/payment_intents'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',  
    'Authorization': 'Bearer sk_test_51Lrs6CK6opjUgeSmFHReX14eBMcbofCJrUOisGTC7ASpkfFMqD6Eysbs83qBC12YZErV3nv1Pg4UTy9WRhPRVUpQ00o7cUrV8I' #Stripe AUTH key
    }
    payload = {
      'amount': 599,
      'currency': 'usd',
      'payment_method': payment_id,
      'confirm': 'true',
      'return_url': 'https://example.com/return'
    }

    #POST request
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        print('Payment Intent - POST request successful!')
        print('Response:', response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print('POST failed:', e)
        print('Response:', response.json())
        return None

#File read function
def read_file(path):
    with open(path, mode='rb') as file:
        return file.read()

    
#----------
if __name__ == '__main__':
    app.run(debug=True)


