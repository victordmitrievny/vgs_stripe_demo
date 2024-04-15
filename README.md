


<p align="center">
     THE PROJECT IS DEPLOYED ON:  <br>
   https://bobham-774de8219399.herokuapp.com/
</p>




_**Description:**_

Bob's Hamburger is a demo app designed to highgligh secure payment processing through VGS data security platform (https://www.verygoodsecurity.com/). 
Whenever users submit their payment card information, the client side uses VGS collect library to securely post the form data to VGS inbound proxy, which tokenizes card number and cvc before passing it to the app's server side.
That way, user's sensitive payment information never gets revealed or stored by the merchant. Then, the server submits tokenized data to Stripe's Create Payment endpoints through VGS outbound proxy which reveals it to the payment processor.
Finally, the data is being posted to Stripe's Payment Intents API thus confirming the transaction and returning the status to the front-end.

<br>
<br>
<br>

_**How to run locally with ngrok:**_ <br>

1. Clone the app files to your own local repository:
   ```bash
   cd "your local repository"
   git clone https://github.com/victordmitrievny/vgs_demo_app/edit/master
   ```
2. Install requirements:
     ```bash
     pip install requirements.txt
     ```
3. Launch _server.py_ file
4. Download and install [ngrok](https://ngrok.com/)
5. Run the following command to start Ngrok and create a tunnel to your local app:
   ```bash
   ngrok http "your port number"
   ```

_**To set up your VGS configurations:**_ <br>

1. Accept invitation to my VGS account
2. Log into our shared VGS sandbox
3. Currently my VGS inbound proxy is configured to pass the form data to the app deployed on Heroku. Change "bobs hamburger - inbound route" Upstream host URL to your ngrok URL.

    <img width="450" alt="Screenshot 2024-04-15 at 2 40 12 AM" src="https://github.com/victordmitrievny/vgs_demo_app/assets/125769590/1f5bf31d-d067-4d8a-a5ee-42113f245ab2">


_**To use the app:**_ <br>
1. Access the app's frontend and submit your payment information to it
2. View logs in the VGS platform AND/OR
3. View **server.py** terminal output to see the results of your submission

 <br>
 <br>
 <br>
 
_**Files Summary:**_ <br>

-form.js - Front-end generation, animations and communication with the VGS inbound proxy <br>
-index.html - Form page <br>
-payment-failure.html - Page generated when payment failed <br>
-payment-success.html - Page generated when payment went through successfully <br>
-styles.css - CSS styles <br>
-server.py - collection of tokenized data, posting through VGS outbound proxy to Payment Methods and then to Payment Intent<br>
-images - images for the HTML page <br>
-Procfile, requirements.txt - supplemental files needed for Heroku deployment <br>
 
