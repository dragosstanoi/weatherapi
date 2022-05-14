"""
WSGI config for wapihome project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

##custom to live server
import sys
import site

# Calculate path to site-packages directory.

python_home = '/usr/www/weatherapi-netshare/venv'

#python_version = '.'.join(map(str, sys.version_info[:2]))
#site_packages = python_home + '/lib/python%s/site-packages' % python_version
site_packages = '/usr/www/weatherapi-netshare/venv/lib/python3.9/site-packages/'

site.addsitedir(site_packages)
site.addsitedir('/usr/www/weatherapi-netshare/weatherapi/backend')

# Remember original sys.path.

prev_sys_path = list(sys.path)


# Reorder sys.path so new directories at the front.

new_sys_path = []

for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)

sys.path[:0] = new_sys_path

##default
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wapihome.settings')

application = get_wsgi_application()
