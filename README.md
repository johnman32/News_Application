# News Application

A Django-based news publishing system with role-based access control for Readers, Journalists, and Editors.

## Features

- Article creation and approval workflow
- Role-based permissions (Reader, Journalist, Editor)
- Newsletter subscriptions
- RESTful API with authentication
- Automated notifications

## Prerequisites

- Python 3.11+
- MySQL (for local development) or Docker
- Git

## Setup Instructions

### Option 1: Running with Virtual Environment

1. Clone the repository:
```
   git clone https://github.com/johnman32/News_Application.git
   cd News_Application
```

2. Create and activate virtual environment:
```
   python3 -m venv venv
   source venv/bin/activate
```
   On Windows: `venv\Scripts\activate`

3. Install dependencies:
```
   pip install -r requirements.txt
```

4. Set up MySQL database:
   - Create a MySQL database named `news_db`
   - Update database credentials in `News_application/settings.py`

5. Run migrations:
```
   python manage.py migrate
```

6. Create a superuser:
```
   python manage.py createsuperuser
```

7. Run the development server:
```
   python manage.py runserver
```

8. Access the application at `http://localhost:8000`

### Option 2: Running with Docker

1. Clone the repository:
```
   git clone https://github.com/johnman32/News_Application.git
   cd News_Application
```

2. Build the Docker image:
```
   docker build -t news-application .
```

3. Run the container:
```
   docker run -p 8000:8000 news-application
```

4. Access the application at `http://localhost:8000`

**Note:** The Docker version uses SQLite instead of MySQL for simplicity.

### Running from Docker Hub

You can pull and run the pre-built image:
```
docker run -p 8000:8000 toobyy/news-application:latest
```

## Security Notes

**IMPORTANT:** Do not commit sensitive information such as:
- Database passwords
- API keys  
- Secret keys

Configure these using environment variables before running the application.

To generate a new Django secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Project Structure
```
News_application/
├── articles/           # Articles app
├── publishers/         # Publishers app
├── users/             # Users app
├── News_application/  # Main project settings
├── templates/         # HTML templates
├── media/            # User-uploaded files
├── docs/             # Sphinx documentation
├── Dockerfile        # Docker configuration
└── requirements.txt  # Python dependencies
```

## Documentation

Generated documentation is available in the `docs/_build/html/` directory.