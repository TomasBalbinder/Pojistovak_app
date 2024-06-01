#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth.models import User
from evidence_pojisteni_app.models import UserProfile  # Importujte váš model UserProfile

username = 'admin'
email = 'tomasbalbinder@gmail.com'
password = 'Idefixa'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username, email, password)
    UserProfile.objects.create(user=user)  # Vytvoříme uživatelský profil
    print(f'Superuser {username} created with profile')
else:
    print(f'Superuser {username} already exists')
EOF