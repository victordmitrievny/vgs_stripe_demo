


**<p align="center">
     The project is deployed on:  <br>
   https://bobham-774de8219399.herokuapp.com/</p>**




_**Description:**_

Bob's Hamburger is a demo app designed to highgligh secure payment processing through VGS data security platform (https://www.verygoodsecurity.com/). 
Whenever users submit their payment card information, the client side uses VGS collect library to securely post the form data to VGS inbound proxy, which tokenizes card number and cvc before passing it to the app's server side.
That way, user's sensitive payment information never gets revealed or stored by the merchant. Then, the server submits tokenized data to Stripe's Create Payment endpoints through VGS outbound proxy which reveals it to the payment processor.
Finally, the data is being posted to Stripe's Payment Intents API thus confirming the transaction and returning the status to the front-end.

<br>
<br>
<br>

**<p align="center">How to Launch, Configure VGS and Use:</p>**


_**How to run locally with ngrok:**_ <br>

1. Clone the app files to your own local repository:
   ```bash
   cd "your project repository"
   git clone https://github.com/victordmitrievny/vgs_demo_app/
   ```
2. Install requirements:
     ```bash
     pip install -r requirements.txt
     ```
3. Launch _server.py_ file in your IDE
4. Create an account on [ngrok](https://ngrok.com/)
5. Install, launch and configure ngrok by following instructions on their website or by running the following commands:
   ```bash
   brew install ngrok/ngrok/ngrok
   ngrok config add-authtoken "your ngrok auth token"
   ngrok http "apps port number"
   ```
6. Confirm that both _server.py_ and your ngrok are running and configured correctly  <br>
 <br>
 <br>
 <br>
 
_**To set up your VGS configurations:**_ <br>

<ins>_If accessing our shared sandbox **(recommended)**:_ </ins> <br>
1. Log into our shared VGS sandbox <br>
2. Navite to "routes" in your vault's administration panel
3. Change "bobs hamburger - inbound route" upstream host URL to your ngrok URL. Currently my VGS inbound proxy is configured to pass the form data to the app deployed on Heroku. <br>

   <img width="450" alt="Screenshot 2024-04-15 at 2 40 12 AM" src="https://github.com/victordmitrievny/vgs_demo_app/assets/125769590/1f5bf31d-d067-4d8a-a5ee-42113f245ab2">  <br>
    <br>

<ins>_If accessing your own VSG sandbox:_ </ins> <br>
1. Navite to "routes" in your vault's administration panel <br>
2. Select "manage" -> "import Yaml file" and import **config.yaml** attached to this project <br>
3. Change "bobs hamburger - inbound route" upstream host URL to your ngrok URL: <br>
<br>
<br>
<br>


_**To use the app:**_ <br>
1. Access the app's frontend and submit your payment information to it
2. View logs in the VGS platform AND/OR  <br>
3. View **server.py** terminal output to see the results of your submission

 <br>
 <br>
 <br>

**<p align="center"> Files Summary: </p>**

-form.js - Front-end generation, animations and communication with the VGS inbound proxy <br>
-index.html - Form page <br>
-payment-failure.html - Page generated when payment failed <br>
-payment-success.html - Page generated when payment went through successfully <br>
-styles.css - CSS styles <br>
-server.py - collection of tokenized data, posting through VGS outbound proxy to Payment Methods and then to Payment Intent<br>
-images - images for the HTML page <br>
-requirements.txt - dependencies <br>
-Procfile - needed for Heorku deployment
 
