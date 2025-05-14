from flask import Flask, request, jsonify
import random
import requests
from config import BASE_URL, BOT_ID, AUTH_TOKEN, PORT

app = Flask(__name__)

# In-memory session storage
user_sessions = {}

# Flag database
flags = {}
scores = {"total": 5, "correct": 0, "wrong": 0, "current": 0}


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
        return f"\nCountry: {data['name']['common']}\nCapital: {data.get('capital', ['Unknown'])[0]}\nRegion: {data['region']}"
    return f"Could not find data for {country_name}"


def get_random_flag():
    country = random.choice(list(flags.keys()))
    return country, flags[country]["url"], flags[country]["hint"]


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    user_id = data.get("conversation_initiated_by")
    user_message = data.get("text", {}).get("body", "").strip().lower()

    if user_message in ["quit", "exit", "stop", "end"]:
        if user_id in user_sessions:
            user_sessions.pop(user_id)
            send_text(user_id,
                      f"🚪 Quiz ended. Final score: {scores['correct']}/{scores['current']}\nType 'flag' to play again!")
        else:
            send_text(user_id, "No active quiz. Type 'flag' to start!")
        return jsonify({"status": "ok"})

    if user_message == "flag":
        reset_quiz(user_id)
        send_welcome_message(user_id)
        return jsonify({"status": "ok"})

    if user_id in user_sessions:
        handle_quiz_answer(user_id, user_message)
    else:
        send_text(user_id, "Welcome to Flag Quiz! 🌍\nType 'flag' to start or 'quit' to exit.")

    return jsonify({"status": "ok"})


def reset_quiz(user_id):
    scores.update({"current": 0, "correct": 0, "wrong": 0})
    user_sessions[user_id] = {"active": True}


def handle_quiz_answer(user_id, user_message):
    session = user_sessions[user_id]
    if not session.get("active"):
        return

    correct_country = session.get("current_country", "").lower()

    # Check if answer is correct (accepts number or country name)
    is_correct = (user_message == correct_country.lower() or
                  user_message == str(session.get("correct_index") + 1))

    if is_correct:
        scores["correct"] += 1
        response = f"✅ Correct! 🎉 {get_country_info(correct_country)}"
    else:
        response = f"❌ Incorrect. The answer was {correct_country.capitalize()}.\n{get_country_info(correct_country)}"

    scores["current"] += 1
    response += f"\n\nScore: {scores['correct']}/{scores['current']}"

    if scores["current"] < scores["total"]:
        response += "\n\nNext question..."
        send_text(user_id, response)
        send_flag_question(user_id)
    else:
        response += "\n\n🏁 Quiz complete! Type 'flag' to play again."
        send_text(user_id, response)
        session["active"] = False


def send_welcome_message(to):
    message = (
        "🌍 Welcome to Flag Quiz!\n"
        "You'll see a flag and 4 options.\n"
        "Reply with the number (1-4) or country name.\n"
        f"Total questions: {scores['total']}\n\n"
        "Type 'quit' anytime to exit.\n"
        "Let's begin!"
    )
    send_text(to, message)
    send_flag_question(to)


def send_flag_question(to):
    country, image_url, hint = get_random_flag()
    user_sessions[to]["current_country"] = country

    # Generate options
    options = [country] + random.sample([c for c in flags if c != country], 3)
    random.shuffle(options)
    user_sessions[to]["correct_index"] = options.index(country)

    # Send flag image
    send_image(to, image_url, "Guess this flag!")

    # Send options
    options_text = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(options)])
    send_text(to,
              f"Question {scores['current'] + 1}/{scores['total']}:\nWhich country's flag is this?\n\nOptions:\n{options_text}")


def send_text(to, message):
    payload = {
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    send_to_swiftchat(payload)


def send_image(to, image_url, caption=""):
    payload = {
        "to": to,
        "type": "image",
        "image": {
            "url": image_url,   # ✅ Corrected from 'link' to 'url'
            "body": caption     # ✅ Corrected from 'caption' to 'body'
        }
    }
    send_to_swiftchat(payload)


def send_to_swiftchat(payload):
    url = f"{BASE_URL}/api/bots/{BOT_ID}/messages"
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Sent to SwiftChat: {response.status_code}")
    except Exception as e:
        print(f"Error sending to SwiftChat: {e}")


if __name__ == '__main__':
    get_all_flags_from_api()
    app.run(port=PORT)