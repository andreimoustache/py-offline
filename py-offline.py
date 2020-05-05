from os import environ, makedirs
from sys import version_info
from urllib.parse import urlparse
from pathlib import Path, PurePath
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

resources = [(path, str(document))]

for resource in own_href_resources:
  url = resource["href"]
  local_url = resource["href"].replace(site_root, "")
  resource["href"] = local_url
  resources.append((local_url, requests.get(url).text))

for resource in own_src_resources:
  url = resource["src"]
  local_url = resource["src"].replace(site_root, "")
  resource["src"] = local_url
  resources.append((local_url, requests.get(url).text))

write_path = Path(f'{environ["PYOFF_DESTINATION"]}/')

print(f'Downloading {len(resources)} resources.')
for (resource, body) in resources:
  filename = PurePath(write_path / resource)
  print(f'Writing file to {filename}.')
  makedirs(filename.parent, exist_ok=True)
  with open(filename, 'w', encoding=response.encoding) as file:
    file.write(body)