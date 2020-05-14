from logging import getLogger
from bs4 import BeautifulSoup
from pyoffline_models import Resource, Document
from beautifulsoup_extensions import has_href_with_url, has_src_with_url


class Parser:
  def __init__(self, site_root: str):
    self.logger = getLogger()
    self.site_root = site_root


  def make_link_relative(self, tag, attribute):
    url = tag[attribute]
    relative_url = tag[attribute].replace(self.site_root, "")
    tag[attribute] = relative_url

    return Resource(url, name=relative_url)


  def detect_resources(self, document, resources):
    own_src_resources = document.find_all(has_href_with_url(self.site_root))
    self.logger.info(f'Found {len(own_src_resources)} href resources tags.')
    resources += [make_link_relative(resource, "href", self.site_root) for resource in own_src_resources]

    own_src_resources = document.find_all(has_src_with_url(self.site_root))
    self.logger.info(f'Found {len(own_src_resources)} src resources tags.')
    resources += [make_link_relative(resource, "src", self.site_root) for resource in own_src_resources]


  def process_document(self, document: Document, resources):
    parsed_document = BeautifulSoup(document.body, "html.parser")
    detect_resources(parsed_document, resources, self.site_root)


  def parse(self, resource: Resource): pass


  def is_resource_writable(self, resource: Resource): pass
