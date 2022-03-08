from django.db import IntegrityError
from user.models import User


def create():
    try:
        User.objects.create_superuser('admin', 'a@a.com', 'admin')
        return "Admin user created"
    except IntegrityError:
        return "Admin user already created, skipping..."
