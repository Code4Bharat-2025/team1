# Flag Quiz Bot

## Problem Statement
Children often struggle to recognize and remember the flags of different countries due to a lack of engaging and interactive learning tools. Traditional methods of memorization can be ineffective and uninspiring, especially for younger learners. There is a need for an educational tool that combines visual learning with gamified interaction to help kids develop better recall and understanding of world flags in a fun, engaging way.

This project aims to develop an interactive bot application that educates kids about country flags through a quiz-based format. The bot will present flag images and ask multiple-choice or hint based questions, providing instant feedback/score and fun facts to reinforce learning. The goal is to make geography more accessible and enjoyable, supporting both informal learning at home and structured education settings.


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

