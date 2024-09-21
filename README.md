
# Negotiation Chatbot

This chatbot simulates a negotiation process between a customer and a supplier using OpenAI's GPT-3.5-turbo model and sentiment analysis (VADER). It follows predefined pricing logic and adapts based on the user's sentiment.

## Features

- **Base Price**: The base price for the product is set at $100.
- **Discounts**: 
  - Default 5% discount (minimum price: $95).
  - If the user is polite (positive sentiment), a 10% discount is applied (minimum price: $90).
- **Offer Evaluation**: 
  - Offers above $100 are rejected.
  - Offers below the minimum price are countered with a request for a higher offer.

## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Satish-Kumar-Verma/Negotiation-Chatbot.git
    cd Negotiation_Chatbot
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

3. **Install the dependencies using requirements.txt**:

    ```bash
    pip install -r requirements.txt
    ```

   The `requirements.txt` file contains all the necessary Python packages to run this project, including Flask for the API server and the OpenAI client.

4. **Set up your OpenAI API key**:

    Open `Negotiation_Chatbot/chatbot/app.py` and replace `"YOUR_API_KEY"` with your actual OpenAI API key.

5. **Run the Flask app**:

    ```bash
    python Negotiation_Chatbot/chatbot/app.py
    ```

6. **Using Postman to Test the API**:

   You can use [Postman](https://www.postman.com/downloads/) to test the API. Below are the available endpoints:

   - `GET /negotiate`: Start the negotiation.
   - `POST /offer`: Make an offer.

### How to Use Postman

1. **Start the Negotiation**:
   - Set up a `GET` request in Postman with the following URL:
     ```
     http://127.0.0.1:5000/negotiate
     ```
   - Send the request to start the negotiation. The bot will respond with an introductory message.

2. **Make an Offer**:
   - Set up a `POST` request in Postman with the following URL:
     ```
     http://127.0.0.1:5000/offer
     ```
   - In the **Body** tab, select **raw** and choose **JSON** format. You can paste the JSON inputs from the provided `negotiation_bot_postman_inputs.txt` file to test different offer scenarios.
   
   Example JSON input:
   ```json
   {
       "offer": 90,
       "message": "I'd like to offer $90. I'm really happy to negotiate."
   }
   ```

3. **Download the JSON Input File**:

   You can download a set of pre-defined inputs to use in Postman from the following link:  
   [negotiation_inputs.txt](https://github.com/Satish-Kumar-Verma/Negotiation-Chatbot/blob/main/chatbot/negotiation_inputs.txt)

---

## Prompt Error and Model Limitations

Sometimes, the bot might generate responses that don't strictly follow the pricing logic. This is due to the usage of the GPT-3.5-turbo model, which can occasionally result in less accurate adherence to predefined logic. Using a more advanced model like GPT-4 can help mitigate these issues and provide more consistent responses.

---

## Demo

You can view the demo of the chatbot in action [here](https://github.com/Satish-Kumar-Verma/Negotiation-Chatbot/blob/main/Demo.mp4). The demo video is located in the `Negotiation_Chatbot/` directory, outside the program folder.

---

## Customization

You can customize the base price, discount percentage, and response templates inside the `PricingLogic` class in `app.py`.
