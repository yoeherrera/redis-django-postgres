# Django Chat Application

This is a real-time chat application built with Django, Channels, PostgreSQL, Redis, and Selenium for testing. The application supports multiple chat rooms, real-time messaging, user authentication, and more.

## Features

- **User Authentication**: Secure login and registration.
- **Real-Time Messaging**: Messages are delivered in real-time using Django Channels and Redis.
- **Multiple Chat Rooms**: Users can create and join multiple chat rooms.
- **Throttling**: Rate limiting to prevent abuse.
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Testing**: Integration and unit tests using Selenium and Django's testing framework.

## Technologies Used

- **Django**: Web framework.
- **Channels**: For WebSocket support and real-time communication.
- **PostgreSQL**: Database.
- **Redis**: Message broker for Channels.
- **Selenium**: For browser automation and testing.

## Installation

### Prerequisites

- Python 3.11
- PostgreSQL
- Redis
- Google Chrome (for Selenium)
- ChromeDriver (for Selenium)

### Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. **Create a virtual environment and activate it:**
   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the dependencies:**
   ```sh
    pip install -r requirements.txt

4. **Configure PostgreSQL:**
    
    - Create a PostgreSQL database and user.
    - Update the DATABASES setting in settings.py with your database credentials.
   
   ```sh
    pip install -r requirements.txt

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. **Configure Redis:**

    Ensure Redis is running on your machine.
    Update the CHANNEL_LAYERS setting in settings.py if necessary.

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('127.0.0.1', 6379)],
            },
        },
    }

6. **Run migrations:**

   ```sh
    python manage.py makemigrations
    python manage.py migrate


7. **Create a superuser:**

   ```sh
    python manage.py createsuperuser

8. **Collect static files:**

   ```sh
    python manage.py collectstatic

9. **Run the development server:**

   ```sh
    python manage.py runserver

## Running Tests

1. Ensure ChromeDriver is installed and available in your PATH.

2. **Run tests:**

    ```sh
    python manage.py test

## Throttling
 
Throttling is enabled to prevent abuse. You can configure the rate limit settings in `settings.py`.

python
Copy code
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/day',  # Adjust the rate limit as needed
    }
}


## Logging

Logging is configured to help with debugging and monitoring. You can adjust the logging settings in `settings.py`.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
For any inquiries, please contact [yoeherrera@gmail.com].

## Project Structure

your-repo/

├── chat/

│   ├── static/

│   │   ├── chat/

│   │   │   ├── css/

│   │   │   │   ├── chat.css

│   │   │   ├── js/

│   │   │   │   ├── main.js

│   ├── templates/

│   │   ├── chat/

│   │   │   ├── base.html

│   │   │   ├── index.html

│   │   │   ├── register.html

│   │   │   ├── login.html

|   |   |   ├── room.html

│   ├── forms.py

│   ├── models.py

│   ├── views.py

│   ├── consumers.py

│   ├── routing.py

├── tests/

│   ├── test_consumers.py

│   ├── test_integration.py

│   ├── test_connection.py

├── manage.py

├── requirements.txt

├── README.md
