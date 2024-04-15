<p align="center">
     THE PROJECT IS DEPLOYED ONLINE AT:  <br>
   https://bobham-774de8219399.herokuapp.com/
</p>

_**Description:**_

Bob's Hamburger is a demo app designed to highgligh secure payment processing through VGS data security platform (https://www.verygoodsecurity.com/). 
When users submit their card information, the client side uses VGS collect library to post the form data securely to VGS inbound proxy, which tokenizes card number and cvc before passing it to the app's server side.
That way, user's sensitive payment information never gets revealed or stored by the merchant. Then, the server submits tokenized data to Stripe's Create Payment endpoints through VGS outbound proxy which reveals it to the payment processor.
Finally, the data is being posted to Stripe's Payment Intents API thus confirming the transaction and returning the status to the front-end.


Some of the main libraries used are: <br>
-VGS collect <br>
-Flask <br>

The project is deployed on Heroku.
 
_**Files Summary:**_ <br>

-form.js - Front-end generation, animations and communication with the backend <br>
-index.html - Form page <br>
-payment-failure.html - Page generated when payment failed <br>
-payment-success.html - Page generated when payment went through successfully <br>
-styles.css - CSS styles <br>
-server.py - collection of tokenized data, posting through VGS outbound proxy to Payment Methods and then to Payment Intent<br>
-images - images for the HTML page <br>
-Procfile, requirements.txt - supplemental files needed for Heroku deployment <br>


To start the program:

1. Pip install requirements.txt
2. Launch **server.py** 

_**Methodology Breakdown:**_

1. The program starts with Python server launch
2. Using HTML and CSS, the program generates basic page layout, its elements, text and the upload button
3. Javascript listens to the image-upload event and passes it to the backend
4. Using Python, the program receives the picture on the back-end
5. Using Tesseract OCR, given the image is in the right format, the program converts the image to a text string
6. The program then formats the text string to make ingredients identification process easier
7. The program then identifies each ingredient by splitting the formatted text string by commas (",") and writes each ingredient in a list of dictionaries
8. The program checks each of the ingredients present in the dictionary against the ingredients present in the SQL database
9. If there is a match, the program generates a dynamic HTML table in Python, and adds the matched ingredient, its category and its effect to a new row
10. The process repeats until the algorithm goes through all of the dictionary ingredients
11. The program passes the resulting HTML table back to Javascript on the front-end
12. Javascript generates the table passed from the back-end and updates the overall HTML layout and CSS styles

13.* The program is then deployed on Heroku, alongside the SQL database created for this project
