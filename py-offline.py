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
  resource = requests.get(url)
  return (local_url, resource.text, resource.encoding)


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

def process_document(site_root, path, resources):
  print(f'Requesting {site_root + path}.')
  response = requests.get(site_root + path)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  document = BeautifulSoup(response.text, "html.parser")
  resources += [(path, str(document), response.encoding)]
  detect_resources(document, resources, site_root)


def main():
  site_url = environ.get("PYOFF_URL", None)
  depth = environ.get("PYOFF_DEPTH", 1)
  write_destination = environ.get("PYOFF_DESTINATION", ".")

  print(f'''
PYOFF_URL={site_url}
PYOFF_DEPTH={depth}
PYOFF_DESTINATION={write_destination}
  ''')

  if site_url is None:
    print("I need a URL, please set the PYOFF_URL environment variable.")
    return exit(1)

  scheme, domain, path, _, _, _ = urlparse(site_url)
  first_path = "index.html" if path in ["/", ""] else path
  site_root = f'{scheme}://{domain}/'
  print(f'Domain set to {domain}.')

  write_path = Path(f'{write_destination}/')
  print(f'Write path set to {write_path}.')

  [write_to_file(write_path, name, body, encoding) for (name, body, encoding) in resources]


if __name__ == "__main__":
  main()
