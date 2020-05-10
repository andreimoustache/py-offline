from os import environ, makedirs
from sys import version_info, exc_info, exit
from urllib.parse import urlparse
from pathlib import Path, PurePath
from pickle import dumps
from pyoffline_downloader import download_resource
from pyoffline_models import Document
from q_publisher import Publisher


def process_site(site_root, first_path, files_publisher: Publisher, resources_publisher: Publisher):
  first_document = Document(site_root+first_path, name=first_path, depth=0)

  documents = [first_document]
  resources = []

  downloaded_documents = [download_resource(document) for document in documents]
  [resources_publisher.publish("resources", document.to_serialised()) for document in downloaded_documents]


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

  write_path = Path(f'./{write_destination}/')
  print(f'Write path set to {write_path}.')

  q_host = environ.get("PYOFF_Q_HOST", "q")
  files_queue_name = environ.get("PYOFF_Q_FILES", "files")
  resources_queue_name = environ.get("PYOFF_Q_RESOURCES", "resources")
  try:
    files_publisher = Publisher(q_host, files_queue_name)
    resources_publisher = Publisher(q_host, resources_queue_name)
    print('Successfully created publishers and subscribers.')
  except:
    print('Failed to create publisher or subscriber.', exc_info())
    exit(1)

  print('Processing site.')
  process_site(site_root, first_path, files_publisher, resources_publisher)


if __name__ == "__main__":
  main()
