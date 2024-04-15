<p align="center">
     THE PROJECT IS DEPLOYED ONLINE AT:  <br>
   https://bobham-774de8219399.herokuapp.com/
</p>

_**Description:**_

Bob's Hamburger is a demo app designed to highgligh secure payment processing through VGS data security platform (https://www.verygoodsecurity.com/). 
Whenever users submit their payment card information, the client side uses VGS collect library to securely post the form data to VGS inbound proxy, which tokenizes card number and cvc before passing it to the app's server side.
That way, user's sensitive payment information never gets revealed or stored by the merchant. Then, the server submits tokenized data to Stripe's Create Payment endpoints through VGS outbound proxy which reveals it to the payment processor.
Finally, the data is being posted to Stripe's Payment Intents API thus confirming the transaction and returning the status to the front-end.

_**To run locally:**_ <br>

1. accept invitation to my VGS account
1. git clone https://github.com/victordmitrievny/vgs_demo_app/edit/master
2. pip install requirements.txt
3. download and install ngrok
4. launch **server.py** file
5. run the following command to start Ngrok and create a tunnel to your local app:
   '''ngrok http your_port_number'''
6. currently my VGS inbound proxy is configured to pass the form data to the app deployed on Heroku. Change **bobs hamburger - inbound route** Upstream host URL to your ngrok URL.
<img width="600" alt="Screenshot 2024-04-15 at 2 40 12 AM" src="https://github.com/victordmitrievny/vgs_demo_app/assets/125769590/1f5bf31d-d067-4d8a-a5ee-42113f245ab2">

7. access the app's frontend and submit your payment information to it.
8. view **server.py** to see the results of your submission
 
_**Files Summary:**_ <br>

-form.js - Front-end generation, animations and communication with the backend <br>
-index.html - Form page <br>
-payment-failure.html - Page generated when payment failed <br>
-payment-success.html - Page generated when payment went through successfully <br>
-styles.css - CSS styles <br>
-server.py - collection of tokenized data, posting through VGS outbound proxy to Payment Methods and then to Payment Intent<br>
-images - images for the HTML page <br>
-Procfile, requirements.txt - supplemental files needed for Heroku deployment <br>
 
