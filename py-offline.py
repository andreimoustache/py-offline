from os import environ, makedirs
from sys import version_info, exit
from urllib.parse import urlparse
from pathlib import Path, PurePath
from pyoffline_writer import write_to_file
from pyoffline_parser import detect_resources, process_document
from pyoffline_downloader import download_document, download_resource


def process_site(site_root, first_path, write_path):
  documents = [(first_path, site_root+first_path)]
  resources = []

  downloaded_documents = [download_document(url, name) for (name, url) in documents]
  [process_document(site_root, path, body, encoding, resources) for (path, body, encoding) in downloaded_documents]

  downloaded_resources = [download_resource(url, name) for (name, url) in resources]
  [write_to_file(write_path, resource) for resource in downloaded_resources]
  [write_to_file(write_path, name, body, encoding) for (name, body, encoding) in downloaded_documents]


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
