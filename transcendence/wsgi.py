import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcendence.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
