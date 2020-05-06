import re
import requests
from bs4 import BeautifulSoup


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


def process_document(site_root, path, body, encoding, resources):
  document = BeautifulSoup(body, "html.parser")
  resources += [(path, str(document), encoding)]
  detect_resources(document, resources, site_root)
