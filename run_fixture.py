import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

fixtures = ['book','comments','tag']
for fixture in fixtures:
    print(f'{fixture}...')
    call_command('loaddata', fixture)