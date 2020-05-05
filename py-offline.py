from os import environ
from sys import version_info
from urllib.parse import urlparse
from pathlib import Path
import re
from bs4 import BeautifulSoup
import requests

print(f'''
PYOFF_URL={environ["PYOFF_URL"]}
PYOFF_DEPTH={environ["PYOFF_DEPTH"]}
PYOFF_DESTINATION={environ["PYOFF_DESTINATION"]}
Running {version_info}''')

scheme, domain, path, _, _, _ = urlparse(environ["PYOFF_URL"])
path = "index.html" if path == "/" else path
site_root = f'{scheme}://{domain}/'

print(f'Domain set to {domain}.')
print(f'Requesting {path}.')
response = requests.get(environ["PYOFF_URL"])
print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

document = BeautifulSoup(response.text, "html.parser")
own_href_resources = document.find_all(href=re.compile(f'^{site_root}'))
own_src_resources = document.find_all(src=re.compile(f'^{site_root}'))
print(f'Found {len(own_href_resources)} href resources tags.')
print(f'Found {len(own_src_resources)} src resources tags.')

for resource in own_href_resources:
  resource["href"] = resource["href"].replace(site_root, "")

for resource in own_src_resources:
  resource["src"] = resource["src"].replace(site_root, "")

write_path = Path(f'{environ["PYOFF_DESTINATION"]}/')
filename = write_path / path
print(f'Writing file to {filename}.')
with open(filename, 'w', encoding=response.encoding) as file:
  file.write(str(document))