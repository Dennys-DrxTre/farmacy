from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}