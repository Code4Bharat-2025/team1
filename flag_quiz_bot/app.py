from flask import Flask, request, jsonify
import random
import requests

app = Flask(__name__)

# In-memory session storage
user_sessions = {}

# Flag database
flags = {}
scores = {"total": 5 , "correct": 0, "wrong": 0,  "current": 0}

def get_all_flags_from_api():
    url = "https://flagcdn.com/en/codes.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch country codes: {response.status_code}")

    code_to_country = response.json()

    for code, country in code_to_country.items():
        flags[country] = {
            "url": f"https://flagcdn.com/w320/{code}.png",
            "hint": f"It starts with '{country[0]}'"
        }

    return flags

def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
        return "\n Country name : " + data["name"]["common"] + "\n  Capital : " + data.get("capital", ["Unknown"])[0] + "\n  Region : " + data["region"] + "\n  Description : " + f"{data['name']['common']} is a country in {data['region']} with its capital at {data.get('capital', ['Unknown'])[0]}."
    else:
        return "error : Could not find data for " + country_name 


# SwiftChat constants
BOT_ID = "Add your bot id here"
SWIFTCHAT_API_URL = "https://v1-api.swiftchat.ai/api/bots/{{BOT_ID}}/messages"
SWIFTCHAT_API_KEY = "21bda582-e8d0-45bc-bb8b-a5c6c555d176"

def get_random_flag():
    country = random.choice(list(flags.keys()))
    return country, flags[country]["url"], flags[country]["hint"]

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received data:", data)

    user_id = data.get("conversation_initiated_by")
    user_message = data.get("text", {}).get("body", "").strip().lower()

    print("User message:", user_message)

    # Always check for 'quit' first
    if user_message == "quit":
        if user_id in user_sessions:
            user_sessions.pop(user_id)
            send_text(user_id, f"👋 Quiz ended. Here are your final scores:\n✅ Correct Answers: {scores['correct']}\n❌ Wrong Answers: {scores['wrong']}\n📊 Total Questions Attempted: {scores['current']}\nType 'flag' anytime to restart!")
        else:
            send_text(user_id, "You're not in a quiz. Type 'flag' to start!")
        return jsonify({"status": "ok"})

    # Start new quiz
    if user_message == "flag":
        scores["current"] = 0
        scores["correct"] = 0
        scores["wrong"] = 0
        send_flag_quiz(user_id)

    # Answering a quiz
    elif user_id in user_sessions:
        correct_country = user_sessions.get(user_id, "").lower()
        info = get_country_info(correct_country)
        if user_message == correct_country:
            scores["correct"] += 1
            scores["current"] += 1
            send_text(user_id, f"✅ Correct! 🎉 {info}\nYour score: {scores['correct']}/{scores['current']}")
        else:
            scores["wrong"] += 1
            scores["current"] += 1
            send_text(user_id, f"❌ Incorrect. The correct answer was {correct_country.capitalize()}." + info + f"\nYour score: {scores['correct']}/{scores['current']}")

        # Continue with next quiz round
        send_flag_quiz(user_id)

    # No quiz in progress
    else:
        send_text(user_id, "Type 'flag' to start the quiz or 'quit' to stop.")

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

    # Save correct answer to session
    user_sessions[to] = country

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
    get_all_flags_from_api()
    app.run(port=5000)
