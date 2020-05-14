import re
from bs4 import BeautifulSoup
from pyoffline_models import Resource, Document


def process_resource(tag, attribute, site_root):
  url = tag[attribute]
  relative_url = tag[attribute].replace(site_root, "")
  tag[attribute] = relative_url

  return Resource(url, name=relative_url)


def detect_resources(document, resources, site_root):
  own_src_resources = document.find_all(href=re.compile(f'^{site_root}'))
  print(f'Found {len(own_src_resources)} href resources tags.')
  resources += [process_resource(resource, "href", site_root) for resource in own_src_resources]

  own_src_resources = document.find_all(src=re.compile(f'^{site_root}'))
  print(f'Found {len(own_src_resources)} src resources tags.')
  resources += [process_resource(resource, "src", site_root) for resource in own_src_resources]


def process_document(site_root, document: Document, resources):
  parsed_document = BeautifulSoup(document.body, "html.parser")
  detect_resources(parsed_document, resources, site_root)


def parse(resource: Resource): pass


def is_resource_writable(resource: Resource): pass
