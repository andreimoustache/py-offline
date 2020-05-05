from os import environ
from sys import version_info
from urllib.parse import urlparse
import requests

print(f'''
PYOFF_URL={environ["PYOFF_URL"]}
PYOFF_DEPTH={environ["PYOFF_DEPTH"]}
PYOFF_DESTINATION={environ["PYOFF_DESTINATION"]}
Running {version_info}''')

_, domain, path, _, _, _ = urlparse(environ["PYOFF_URL"])

print(f'Domain set to {domain}.')
print(f'Requesting {path}.')
response = requests.get(environ["PYOFF_URL"])
print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')