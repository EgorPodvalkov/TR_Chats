# TR Chat

TR Chat is a web application that allows users to create and manage workspaces for chat conversations. Users can invite others to join their workspaces and create chat rooms for text-based conversations.

## Features

- User authentication and authorization
- Creation and management of workspaces and channles in it
- Invite other users to join workspaces
- Real-time chat functionality

## Tech Stack

- Python (Flask, sqlite3)
- JavaScript
- HTML/CSS

## Installation

1. Clone the repository: `git clone https://github.com/EgorPodvalkov/TR_Chats.git`
2. Create two virtual environments:
   - frontEnv
      1. Go to Frontend folder and create virtual env: `python -m venv frontvEnv`
      2. Activate the virtual environment:
         - Windows: `.\Frontend\frontvEnv\Scripts\activate`
         - macOS/Linux: `source Frontend/frontvEnv/bin/activate`
      3. Install the dependencies: `pip install -r requirements.txt`
   - backEnv
      1. Go to Backend folder and create virtual env: `python -m venv backEnv`
      2. Activate the virtual environment:
         - Windows: `.\Backend\backEnv\Scripts\activate`
         - macOS/Linux: `source Backend/backEnv/bin/activate`
      3. Install the dependencies: `pip install -r requirements.txt`
      4. Create telegram bot and email
      5. Create Backend/.env file and enter your BOT_EMAIL, BOT_EMAIL_PASSWORD and BOT_TELEGRAM_API constants
3. Run the application in Frontend folder with a web server for frontend: `python webserver.py`
4. Run the application in Backend folder with a web server for managing database: `python webserver.py`
5. Run the application in Backend folder that launches telegram bot for notifications and verification codes: `python sender/telegramBot.py`
6. Open a web browser and navigate to http://127.0.0.1:8080 or to http://{your ip adress}:8080

### Usage

1. Navigate to http://127.0.0.1:8080 or to http://{your ip adress}:8080 in your web browser.
2. Register for a new account or log in to an existing one.
3. Create a new workspace or join an existing one by entering its invite code.
4. Create a new chat room within a workspace or join an existing one.
5. Start chatting! 😁

### Author

 - Egor Podvalkov
