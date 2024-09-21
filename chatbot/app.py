from flask import Flask, request, jsonify
from openai import OpenAI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize OpenAI Client
client = OpenAI(api_key="YOUR_API_KEY") 

# Initialize Flask app
app = Flask(__name__)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Pricing logic class to handle offers
class PricingLogic:
    def __init__(self, base_price):
        self.base_price = base_price
        self.min_discount = 0.95  # 5% discount
        self.max_discount = 0.9  # 10% discount (for polite users)
        self.min_price = base_price * self.min_discount  # Minimum price after 5% discount

    def evaluate_offer(self, offer, sentiment):
        # If the sentiment is positive (polite), offer up to a 10% discount
        if sentiment == "positive":
            self.min_price = self.base_price * self.max_discount  # Adjust to 10% off

        if offer >= self.base_price:  # If the offer is more than the base price
            return "reject_high", self.base_price  # Offer base price
        elif offer >= self.min_price and offer < self.base_price:  # Acceptable offer range
            return "accept", offer
        elif offer < self.min_price:  # Offer too low
            return "reject_low", self.min_price
        else:
            return "counter", None  # Fallback case (this shouldn't happen based on logic)

# Initialize pricing logic for a product
pricing = PricingLogic(base_price=100)  # Base price of $100

# Function to analyze sentiment using VADER
def analyze_sentiment(user_message):
    sentiment_score = analyzer.polarity_scores(user_message)
    if sentiment_score['compound'] >= 0.05:
        return "positive"
    elif sentiment_score['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

# Function to generate response from OpenAI's ChatCompletion API
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use GPT-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a negotiation bot, handling price discussions. Never offer a price higher than the original price, and strictly follow the base price and discounts."},
            {"role": "user", "content": prompt}
        ]
    )
    message = response.choices[0].message.content.strip()
    return message

# Endpoint to start negotiation
@app.route('/negotiate', methods=['GET'])
def start_negotiation():
    return jsonify({"message": "Hello! Let's negotiate the price of the product."})

# Endpoint to receive user's offer and respond
@app.route('/offer', methods=['POST'])
def receive_offer():
    data = request.json
    user_offer = data.get('offer')
    user_message = data.get('message', "")

    # Analyze sentiment of user's message
    sentiment = analyze_sentiment(user_message)

    # Evaluate the user's offer with sentiment taken into account
    status, result = pricing.evaluate_offer(user_offer, sentiment)

    # Determine response based on the evaluation
    if status == "accept":
        response_text = f"We accept your offer of ${user_offer}."
    elif status == "reject_high":
        response_text = f"Reject: Thank you for your offer, but we cannot accept more than the original price of ${pricing.base_price}. Let's stick with the original price."
    elif status == "reject_low":
        response_text = f"Reject: Your offer is too low. Could you increase it to at least ${result}?"
    else:
        response_text = f"Reject: ow about we meet halfway with a price of ${result}?"

    # Log the prompt to verify control over response
    print(f"Generated Response: {response_text}")

    # Generate AI-powered response, but strictly pass the controlled response as the prompt
    conversation = generate_response(response_text)

    return jsonify({
        "bot_response": conversation,
        "sentiment": sentiment
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
