from flask import Flask, request, jsonify
import random
import uuid
import requests

app = Flask(__name__)

# Flag database
flags = {
    "India": {
        "url": "https://flagcdn.com/w320/in.png",
        "hint": "It starts with 'I'"
    },
    "Germany": {
        "url": "https://flagcdn.com/w320/de.png",
        "hint": "It starts with 'G'"
    },
    "France": {
        "url": "https://flagcdn.com/w320/fr.png",
        "hint": "It starts with 'F'"
    },
    "Japan": {
        "url": "https://flagcdn.com/w320/jp.png",
        "hint": "It starts with 'J'"
    }
}

# SwiftChat constants
SWIFTCHAT_API_URL = "https://v1-api.swiftchat.ai/api/bots/0296329455117838/messages"
SWIFTCHAT_API_KEY = "21bda582-e8d0-45bc-bb8b-a5c6c555d176"

def get_random_flag():
    country = random.choice(list(flags.keys()))
    return country, flags[country]["url"], flags[country]["hint"]

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    conversation_initiated_by = data.get("conversation_initiated_by")
    user_message = data.get("text", {}).get("body", "").lower()

    print("User message:", user_message)
    
    if user_message == "flag":
        send_flag_quiz(conversation_initiated_by)
    else:
        send_text(conversation_initiated_by, "Type 'flag' to start the quiz!")

    return jsonify({"status": "ok"})

def send_text(to, message):
    payload = {
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    send_to_swiftchat(payload)

def send_flag_quiz(to):
    country, image_url, hint = get_random_flag()

    messages = [
        {
            "to": to,
            "type": "text",
            "text": {
                "body": "🌍 Can you guess which country's flag this is?"
            }
        },
        {
            "to": to,
            "type": "image",
            "image": {
                "url": image_url,
                "body": "Here's the flag!"
            },
            "rating_type": "thumb"
        },
        {
            "to": to,
            "type": "text",
            "text": {
                "body": f"Hint: {hint}"
            }
        }
    ]

    for msg in messages:
        send_to_swiftchat(msg)

def send_to_swiftchat(payload):
    headers = {
        "Authorization": f"Bearer {SWIFTCHAT_API_KEY}",
        "API-Key": SWIFTCHAT_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(SWIFTCHAT_API_URL, headers=headers, json=payload)
        print("Sent to SwiftChat:", payload)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending to SwiftChat:", e)

if __name__ == '__main__':
    app.run(port=5000)
