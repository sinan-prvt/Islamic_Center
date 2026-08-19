"""
WSGI config for skssf_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
orig_db = BASE_DIR / 'db.sqlite3'
tmp_db = Path('/tmp') / 'db.sqlite3'

if orig_db.exists() and (not tmp_db.exists() or tmp_db.stat().st_size == 0):
    try:
        shutil.copy2(orig_db, tmp_db)
        os.chmod(tmp_db, 0o666)
    except Exception as e:
        print(f"Error copying DB in wsgi: {e}")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skssf_portal.settings')

application = get_wsgi_application()
app = application

# Automatically migrate & seed default superuser when running in production/serverless
IS_SERVERLESS = os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or '/var/task' in str(BASE_DIR)
if IS_SERVERLESS or os.environ.get('DATABASE_URL'):
    try:
        from django.core.management import call_command
        from django.contrib.auth.models import User
        call_command('migrate', interactive=False)
        if not User.objects.filter(is_staff=True).exists():
            User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
    except Exception as e:
        print(f"Error initializing production database: {e}")



