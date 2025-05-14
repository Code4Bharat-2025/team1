# Flag Quiz Bot

This is a simple Flask-based chatbot backend that interacts with SwiftChat for a flag quiz game.

## Problem Statement -
Children often struggle to recognize and remember the flags of different countries due to a lack of engaging and interactive learning tools. Traditional methods of memorization can be ineffective and uninspiring, especially for younger learners. There is a need for an educational tool that combines visual learning with gamified interaction to help kids develop better recall and understanding of world flags in a fun, engaging way.

This project aims to develop an interactive bot application that educates kids about country flags through a quiz-based format. The bot will present flag images and ask multiple-choice or hint based questions, providing instant feedback/score and fun facts to reinforce learning. The goal is to make geography more accessible and enjoyable, supporting both informal learning at home and structured educational settings.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Webhook Endpoint
- POST `/webhook` — expects JSON payload with `userId` and `message`.