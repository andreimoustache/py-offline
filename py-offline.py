from os import environ
from sys import version_info
from urllib.parse import urlparse
from pathlib import Path
import requests

print(f'''
PYOFF_URL={environ["PYOFF_URL"]}
PYOFF_DEPTH={environ["PYOFF_DEPTH"]}
PYOFF_DESTINATION={environ["PYOFF_DESTINATION"]}
Running {version_info}''')

_, domain, path, _, _, _ = urlparse(environ["PYOFF_URL"])
path = "index.html" if path == "/" else path

print(f'Domain set to {domain}.')
print(f'Requesting {path}.')
response = requests.get(environ["PYOFF_URL"])
print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

write_path = Path(f'{environ["PYOFF_DESTINATION"]}/')
filename = write_path / path
print(f'Writing file to {filename}.')
with open(filename, 'w', encoding=response.encoding) as file:
  file.write(response.text)