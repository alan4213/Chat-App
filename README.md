# Django Real-Time Chat Application

A real-time chat application built with Django, Django Channels, and WebSocket for instant messaging between users.

##  Features

- **User Authentication**: Register, login, and logout functionality
- **Real-Time Messaging**: WebSocket-based instant messaging
- **Online Status**: Green dot indicator for online users
- **Read Receipts**: ✓ for sent messages, ✓✓ for read messages
- **Typing Indicator**: See when the other user is typing
- **Unread Message Count**: Badge showing unread messages from each user
- **Message History**: All messages are saved and displayed
- **Delete Messages**: Users can delete their own messages
- **Auto-Scroll**: Automatically scrolls to the latest message
- **Last Seen**: Shows when offline users were last active

## Tech Stack

- **Backend**: Python, Django 4.2
- **Real-Time**: Django Channels, WebSocket
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Architecture**: MVT (Model-View-Template)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation & Setup

### 1. Clone the Repository


### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

##  Usage

1. **Register**: Create a new account at `/register/`
2. **Login**: Sign in with your credentials at `/login/`
3. **User List**: View all registered users with online status
4. **Start Chat**: Click on any user to open a private chat
5. **Send Messages**: Type and send real-time messages
6. **Read Status**: Messages show ✓ when sent and ✓✓ when read
7. **Delete**: Hover over your messages to see delete option
8. **Logout**: Click logout to end your session

