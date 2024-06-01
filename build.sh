#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
    echo "Vytvářím superuživatele..."
    python manage.py createsuperuser --no-input --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"
    
    echo "Kontroluji a vytvářím UserProfile..."
    python << END
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pojistovna.settings')
import django
django.setup()
from django.contrib.auth.models import User
from evidence_pojisteni_app.models import UserProfile

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
user = User.objects.get(username=username)
UserProfile.objects.get_or_create(user=user)
END
fi
