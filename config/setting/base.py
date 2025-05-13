from pathlib import Path

import dotenv
import os

dotenv.load_dotenv()

env = os.environ.get

BASE_DIR = Path(__file__).resolve().parent.parent

# Debug mode setting
DEBUG = env("DEBUG") == 'True'
# DEBUG = True
# Deployment environment setting
deploy = env("deploy",default=False)

# Secret key for security purposes
SECRET_KEY = env("SECRET_KEY")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
