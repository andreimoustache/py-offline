import logging
from os import environ, makedirs
from sys import version_info, exc_info, exit
from threading import Thread
from urllib.parse import urlparse
from pathlib import Path, PurePath
from pickle import dumps
from pyoffline_downloader import download_resource
from pyoffline_models import Document
from q_publisher import Publisher


def process_site(site_root, first_path, resources_publisher: Publisher):
  first_document = Document(site_root+first_path, name=first_path, depth=0)

  documents = [first_document]
  resources = []

  downloaded_documents = [download_resource(document) for document in documents]
  [resources_publisher.publish("resources", document.to_serialised()) for document in downloaded_documents]


def main():
  log_format = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s %(lineno) -5d: %(message)s')
  logging.basicConfig(level=logging.DEBUG, format=log_format)
  logger = logging.getLogger(__name__)

  site_url = environ.get("PYOFF_URL", None)
  depth = environ.get("PYOFF_DEPTH", 1)
  write_destination = environ.get("PYOFF_DESTINATION", ".")

  logger.info(f'''
PYOFF_URL={site_url}
PYOFF_DEPTH={depth}
PYOFF_DESTINATION={write_destination}
  ''')

  if site_url is None:
    logger.error("I need a URL, please set the PYOFF_URL environment variable.")
    return exit(1)

  scheme, domain, path, _, _, _ = urlparse(site_url)
  first_path = "index.html" if path in ["/", ""] else path
  site_root = f'{scheme}://{domain}/'
  logger.info(f'Domain set to {domain}.')

  write_path = Path(f'./{write_destination}/')
  logger.info(f'Write path set to {write_path}.')

  q_host = environ.get("PYOFF_Q_HOST", "q")
  q_port = environ.get("PYOFF_Q_PORT", "5672")
  files_queue_name = environ.get("PYOFF_Q_FILES", "files")
  resources_queue_name = environ.get("PYOFF_Q_RESOURCES", "resources")
  try:
    resources_publisher = Publisher(q_host, q_port, resources_queue_name)
    logger.info('Successfully created publishers and subscribers.')
  except:
    logger.error('Failed to create publisher or subscriber.', exc_info())
    exit(1)

  publisher_thread = Thread(target=resources_publisher.run, daemon=True)
  publisher_thread.start()

  logger.info('Processing site.')
  process_site(site_root, first_path, resources_publisher)


if __name__ == "__main__":
  main()
