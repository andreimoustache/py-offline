from logging import getLogger
from bs4 import BeautifulSoup
from pyoffline_models import Resource, Document
from beautifulsoup_extensions import has_href_with_url, has_src_with_url
from url_extensions import make_url_absolute, make_url_relative


class Parser:
  def __init__(self, site_root: str):
    self.logger = getLogger()
    self.site_root = site_root


  def process_link(self, tag, attribute, current_depth=0):
    absolute_url = make_url_absolute(self.site_root, tag[attribute])
    relative_url = make_url_relative(self.site_root, tag[attribute])
    tag[attribute] = relative_url

    if tag.name == "a":
      resource = Document(absolute_url, name=relative_url, depth=current_depth+1)
    else:
      resource = Resource(absolute_url, name=relative_url)

    return resource


  def detect_resources(self, document, current_depth):
    resources = []

    href_tags = document.find_all(has_href_with_url(self.site_root))
    self.logger.info(f'Found {len(href_tags)} href resources tags.')
    resources += [self.process_link(tag, "href",current_depth) for tag in href_tags]

    src_tags = document.find_all(has_src_with_url(self.site_root))
    self.logger.info(f'Found {len(src_tags)} src resources tags.')
    resources += [self.process_link(resource, "src", current_depth) for resource in src_tags]

    return resources


  def parse(self, resource: Document):
    parsed_resource = BeautifulSoup(resource.body, "html.parser")
    detected_resources = self.detect_resources(parsed_resource, resource.depth)

    resource.body = str(parsed_resource)

    return [resource] + detected_resources


  def is_resource_writable(self, resource: Resource):
    has_body = resource.body is not None
    needs_processing = resource.mimeType == "text/html"
    return has_body and not needs_processing
