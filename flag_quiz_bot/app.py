from flask import Flask, request, jsonify
import random
import uuid

app = Flask(__name__)

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

def get_random_flag():
    country = random.choice(list(flags.keys()))
    return country, flags[country]["url"], flags[country]["hint"]

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    user_message = data.get("text", {}).get("body", "").lower()
    user_id = data.get("user", {}).get("id", "anonymous")

    if user_message == "flag":
        country, image_url, hint = get_random_flag()
        messages = [
            {
                "type": "text",
                "text": "🌍 Can you guess which country's flag this is?",
                "message_id": str(uuid.uuid4()),
                "user_id": user_id
            },
            {
                "type": "image",
                "image": {
                    "url": image_url
                },
                "message_id": str(uuid.uuid4()),
                "user_id": user_id
            },
            {
                "type": "text",
                "text": f"Hint: {hint}",
                "message_id": str(uuid.uuid4()),
                "user_id": user_id
            }
        ]
    else:
        messages = [
            {
                "type": "text",
                "text": "Type 'flag' to start the quiz!",
                "message_id": str(uuid.uuid4()),
                "user_id": user_id
            }
        ]

    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(port=5000)
