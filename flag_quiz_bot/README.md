# Flag Quiz Bot

This is a simple Flask-based chatbot backend that interacts with SwiftChat for a flag quiz game.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Webhook Endpoint
- POST `/webhook` — expects JSON payload with `userId` and `message`.