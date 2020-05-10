from os import environ
from sys import exc_info, exit
from bs4 import BeautifulSoup
from pyoffline_models import Resource, Document
from beautifulsoup_extensions import has_href_with_own_url, has_src_with_own_url
from urllib.parse import urlparse
from q_consumer import Consumer
from q_publisher import Publisher


class Parser:
  def __init__(self, site_root, publisher: Publisher, consumer: Consumer):
    self.site_root = site_root
    self.publisher = publisher
    self.consumer = consumer


  def start_consuming(self):
    while True:
      self.consumer.run()


  def make_link_relative(self, tag, attribute):
    url = tag[attribute]
    relative_url = tag[attribute].replace(self.site_root, "")
    tag[attribute] = relative_url

    return Resource(url, name=relative_url)


  def detect_resources(self, document):
    own_href_resources = document.find_all(has_href_with_own_url(self.site_root))
    print(f'Found {len(own_href_resources)} href resources tags.')
    [self.make_link_relative(resource, "href", site_root) for resource in own_href_resources]

    own_src_resources = document.find_all(has_src_with_own_url(self.site_root))
    print(f'Found {len(own_src_resources)} src resources tags.')
    [self.make_link_relative(resource, "src", site_root) for resource in own_src_resources]

    return own_href_resources + own_src_resources


  def process_document(self, document: Document):
    document.body = BeautifulSoup(document.body, "html.parser")
    found_resources = detect_resources(document.body)

    return (document, found_resources)


  def parse_resource(self, resource: Resource):
    if resource.mimeType == "text/html":
      (document, resources) = self.process_document(resource)
      self.publisher.publish("files", document.to_serialised())
      [self.publisher.publish("files", resource.to_serialised()) for resource in resources]
    else:
      self.publisher.publish("files", resource.to_serialised())


  def consumer_callback(self, body):
    resource = Resource.from_serialised(body)
    print(" [x] Received %r" % resource.name)
    self.parse_resource(resource)


if __name__ == '__main__':
  site_url = environ.get("PYOFF_URL", None)
  depth = environ.get("PYOFF_DEPTH", 1)
  queue_host = environ.get("PYOFF_Q_HOST", "q")
  files_queue_name = environ.get("PYOFF_Q_FILES", "files")
  resources_queue_name = environ.get("PYOFF_Q_RESOURCES", "resources")

  scheme, domain, _, _, _, _ = urlparse(site_url)
  site_root = f'{scheme}://{domain}/'
  print(f'Domain set to {domain}.')

  try:
    publisher = Publisher(queue_host, files_queue_name)
    print('Successfully created publisher.')
  except:
    print('Failed to create publisher.', exc_info())
    exit(1)

  try:
    consumer = Consumer(queue_host, resources_queue_name)
    print('Successfully created consumer.')
  except:
    print('Failed to create consumer.', exc_info())
    exit(1)


  parser = Parser(site_root, publisher, consumer)
  parser.start_consuming()
