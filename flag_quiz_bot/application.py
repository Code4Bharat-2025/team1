import json
import random
import requests
from flask import Flask, render_template, request

import ssl
print(ssl.OPENSSL_VERSION)

app = Flask(__name__)

# SwiftChat API setup
SWIFTCHAT_API_KEY = '21bda582-e8d0-45bc-bb8b-a5c6c555d176'  # Replace with your actual key
SWIFTCHAT_CHAT_API_URL = 'https://v1-api.swiftchat.ai/api/bot'  # ✅ Correct endpoint for chat

# A list of flags with country names and image URLs
flags = [
    {"country": "USA", "flagUrl": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Flag_of_the_United_States.svg"},
    {"country": "Canada", "flagUrl": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Canada.svg"},
    {"country": "India", "flagUrl": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"},
    # Add more flags as needed
]

def send_to_swiftchat(message, context=None):
    """
    Function to send user input to SwiftChat API and get the response.
    """
    headers = {
        'Authorization': f'Bearer {SWIFTCHAT_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "message": message,
        "context": context or {}
    }

    try:
        response = requests.post(SWIFTCHAT_CHAT_API_URL, headers=headers, data=json.dumps(data), verify=False)

        if response.status_code == 200:
            return response.json()  # Return SwiftChat response
        else:
            print("SwiftChat error:", response.status_code, response.text)
            return {'message': 'Error: Unable to contact SwiftChat API'}
    except Exception as e:
        print("Exception occurred while calling SwiftChat:", e)
        return {'message': 'Error: Unable to contact SwiftChat API'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-flag')
def get_flag():
    flag = random.choice(flags)
    context = {"flag": flag["country"]}

    swiftchat_response = send_to_swiftchat(
        f"Guess the country for this flag: {flag['country']}", context)

    return json.dumps({
        "flag": flag["country"],
        "flagUrl": flag["flagUrl"],
        "swiftchat_message": swiftchat_response.get('message', 'Your flag question is ready!'),
    })

@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    print(f"Received data: {data}")

    if not data or 'answer' not in data or 'flag' not in data:
        return json.dumps({
            "isCorrect": False,
            "message": "Missing required data (answer or flag). Please try again.",
        })

    user_answer = data.get('answer', '').strip().lower()
    correct_answer = data.get('flag', '').strip().lower()

    swiftchat_response = send_to_swiftchat(
        f"User guessed: {user_answer}. Correct answer: {correct_answer}.")

    if user_answer == correct_answer:
        return json.dumps({
            "isCorrect": True,
            "message": "Correct! Well done!",
            "swiftchat_message": swiftchat_response.get('message', '')
        })
    else:
        return json.dumps({
            "isCorrect": False,
            "message": f"Incorrect. The correct answer was {correct_answer}.",
            "swiftchat_message": swiftchat_response.get('message', '')
        })
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    


@app.route('/', methods=['POST'])
def handle_swiftchat_webhook():
    data = request.get_json()
    print("SwiftChat incoming:", data)

    return json.dumps({
        "reply": "Thanks for your message!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
