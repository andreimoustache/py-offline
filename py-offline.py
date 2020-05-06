from os import environ, makedirs
from sys import version_info
from urllib.parse import urlparse
from pathlib import Path, PurePath
import re
from bs4 import BeautifulSoup
import requests


def process_resource(tag, attribute, site_root):
  url = tag[attribute]
  local_url = tag[attribute].replace(site_root, "")
  tag[attribute] = local_url
  return (local_url, requests.get(url).text)


def detect_resources(document, resources, site_root):
  own_src_resources = document.find_all(href=re.compile(f'^{site_root}'))
  print(f'Found {len(own_src_resources)} href resources tags.')
  resources += [process_resource(resource, "href", site_root) for resource in own_src_resources]

  own_src_resources = document.find_all(src=re.compile(f'^{site_root}'))
  print(f'Found {len(own_src_resources)} src resources tags.')
  resources += [process_resource(resource, "src", site_root) for resource in own_src_resources]


def write_to_file(path, name, body, encoding):
  filename = PurePath(path / name)
  print(f'Writing file to {filename}.')
  makedirs(filename.parent, exist_ok=True)
  with open(filename, 'w', encoding=encoding) as file:
    file.write(body)


def main():
  print(f'''
PYOFF_URL={environ["PYOFF_URL"]}
PYOFF_DEPTH={environ["PYOFF_DEPTH"]}
PYOFF_DESTINATION={environ["PYOFF_DESTINATION"]}
Running {version_info}
  ''')

  scheme, domain, path, _, _, _ = urlparse(environ["PYOFF_URL"])
  path = "index.html" if path == "/" else path
  site_root = f'{scheme}://{domain}/'
  print(f'Domain set to {domain}.')

  print(f'Requesting {path}.')
  response = requests.get(environ["PYOFF_URL"])
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  document = BeautifulSoup(response.text, "html.parser")
  resources = [(path, str(document))]
  detect_resources(document, resources, site_root)

  write_path = Path(f'{environ["PYOFF_DESTINATION"]}/')
  print(f'Writing files to {write_path}.')

  print(f'Downloading {len(resources)} resources.')
  [write_to_file(write_path, name, body, response.encoding) for (name, body) in resources]


if __name__ == "__main__":
  main()
