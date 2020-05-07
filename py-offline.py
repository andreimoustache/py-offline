from os import environ, makedirs
from sys import version_info, exit
from urllib.parse import urlparse
from pathlib import Path, PurePath
from pyoffline_writer import write_to_file
from pyoffline_parser import detect_resources, process_document
from pyoffline_downloader import download_resource
from pyoffline_models import Document


def process_site(site_root, first_path, write_path):
  first_document = Document(site_root+first_path, name=first_path, depth=0)

  documents = [first_document]
  resources = []

  downloaded_documents = [download_resource(document) for document in documents]
  [process_document(site_root, document, resources) for document in downloaded_documents]

  downloaded_resources = [download_resource(resource) for resource in resources]
  [write_to_file(write_path, resource) for resource in downloaded_resources]
  [write_to_file(write_path, document) for document in downloaded_documents]


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

  process_site(site_root, first_path, write_path)


if __name__ == "__main__":
  main()
