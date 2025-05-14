# FlagFrenzy-Bot
This is a simple Flask-based chatbot backend that interacts with SwiftChat for a flag quiz game.

## Problem Statement
Children often struggle to recognize and remember the flags of different countries due to a lack of engaging and interactive learning tools. Traditional methods of memorization can be ineffective and uninspiring, especially for younger learners. There is a need for an educational tool that combines visual learning with gamified interaction to help kids develop better recall and understanding of world flags in a fun, engaging way.

This project aims to develop an interactive bot application that educates kids about country flags through a quiz-based format. The bot will present flag images and ask multiple-choice or hint based questions, providing instant feedback/score and fun facts to reinforce learning. The goal is to make geography more accessible and enjoyable, supporting both informal learning at home and structured education settings.

## Key Features of the FlagFrenzy-Bot App
1. Interactive Image-Based Bot
   A fun and engaging chatbot that uses vivid images of country flags to make learning visually appealing and interactive for kids.

2. Multiple Quiz Formats
   Offers quizzes in different formats—select the correct answer from multiple choices or get a hit to guess the answer to make learning playful and dynamic.

3. Instant Feedback on Answers
   Provides real-time feedback after each question, indicating whether the answer is correct or incorrect to reinforce understanding immediately.

4. Educational Insights
   Shares interesting facts about each country and its flag after every question to deepen knowledge and spark curiosity.

5. Score Tracking and Display
   Displays the final quiz score at the end of each session to motivate kids and help track their progress.

## Setup

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:

    ```bash
    python app.py
    ```

## Webhook Endpoint

- **POST `/webhook`** — Expects a JSON payload with the following parameters:
  - `userId`: The ID of the user.
  - `message`: The message sent by the user.

## Prerequisites

- Install Python.
- Install [ngrok](https://ngrok.com/).

## Steps to Run

1. Run `app.py`:

    ```bash
    python app.py
    ```

2. Start ngrok to expose the local server:

    ```bash
    ngrok http 5000
    ```

3. Update the webhook URL using the Swift Chat API.

4. Go to [Convegenius Web](https://web.convegenius.ai/home) and select the bot to start.

## Help using the bot:
Give "flag" as input command to start the quiz and "quit" command to stop the quiz at anytime


