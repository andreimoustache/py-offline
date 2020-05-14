from os import environ
from sys import version_info, exit
from threading import Thread
import logging
from config import Config, ConfigException
from pyoffline_writer import write
from pyoffline_parser import parse, is_resource_writable
from pyoffline_downloader import download


def process_site(site_root, documents, resources, files, first_path, write_path):
  first_document = Document(site_root+first_path, name=first_path, depth=0)

  documents.append(first_document)

  downloaded_documents = [download_resource(document) for document in documents]
  [process_document(site_root, document, resources) for document in downloaded_documents]

  downloaded_resources = [download_resource(resource) for resource in resources]
  [write_to_file(write_path, resource) for resource in downloaded_resources]
  [write_to_file(write_path, document) for document in downloaded_documents]


def main(logger: logging.Logger):
  try:
    config = Config(environ)
  except ConfigException as ex:
    logger.fatal(ex.args)
    return exit(1)

  logger.info("Starting py-offline")
  logger.info(config)

  documents, resources, files = [], [], []
  process_site(config.site_root, documents, resources, files, config.first_path, config.write_path)


if __name__ == "__main__":
  log_format = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s %(lineno) -5d: %(message)s')
  logging.basicConfig(level=logging.INFO, format=log_format)
  logger = logging.getLogger(__name__)

  main(logger)
