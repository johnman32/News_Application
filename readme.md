# News Application

A Django-based news publishing system with role based access control for Readers, Journalists, and Editors.

## Features

- Article creation and approval workflow
- Role-based permissions 
- Newsletter subscriptions
- RESTful API with authentication
- Automated notifications

## Prerequisites

- Python 3.11+
- MySQL (for local development) or Docker
- Git

## Setup Instructions

### Option 1: Running with Virtual Environment 

1. **Clone the repository:**
```bash
   git clone <your-repo-url>
   cd News_application
```

2. **Create and activate virtual environment:**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Set up MySQL database:**
   - Create a MySQL database named `news_db`
   - Update `News_application/settings.py` with your MySQL credentials:
```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'news_db',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
```

5. **Run migrations:**
```bash
   python manage.py migrate
```

6. **Create a superuser:**
```bash
   python manage.py createsuperuser
```

7. **Run the development server:**
```bash
   python manage.py runserver
```

8. **Access the application:**
   - Open your browser to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

### Option 2: Running with Docker

1. **Clone the repository:**
```bash
   git clone <your-repo-url>
   cd News_application
```

2. **Build the Docker image:**
```bash
   docker build -t news-application .
```

3. **Run the container:**
```bash
   docker run -p 8000:8000 news-application
```

4. **Access the application:**
   - Open your browser to `http://localhost:8000`

**Note:** The Docker version uses SQLite instead of MySQL.


## Security Notes

Before running the application, you must:
1. Set your own `SECRET_KEY` in `News_application/settings.py`
2. Configure your database credentials
3. Never commit sensitive credentials to version control

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

To rebuild documentation:
```bash
cd docs
make html
```
