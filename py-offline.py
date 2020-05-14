from os import environ
from queue import Queue
from sys import version_info, exit
from threading import Thread
import logging
from config import Config, ConfigException
from pyoffline_writer import write
from pyoffline_parser import parse, is_resource_writable
from pyoffline_downloader import download
from pyoffline_models import Document, Resource
from queue_processors import processor, fork_processor


def process_site(site_root, urls, resources, files, first_path, write_path):
  first_document = Document(site_root+first_path, name=first_path, depth=0)

  urls.put(first_document)

  download_processor_args = (urls, download, resources)
  parse_processor_args = (resources, parse, is_resource_writable, files, urls)
  write_processor_args = (files, write)

  Thread(target=processor, args=download_processor_args, daemon=True).start()
  Thread(target=fork_processor, args=parse_processor_args, daemon=True).start()
  Thread(target=processor, args=write_processor_args, daemon=True).start()


def main(logger: logging.Logger):
  try:
    config = Config(environ)
  except ConfigException as ex:
    logger.fatal(ex.args)
    return exit(1)

  logger.info("Starting py-offline")
  logger.info(config)

  urls, resources, files = Queue(), Queue(), Queue()
  process_site(config.site_root, urls, resources, files, config.first_path, config.write_path)


if __name__ == "__main__":
  log_format = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s %(lineno) -5d: %(message)s')
  logging.basicConfig(level=logging.INFO, format=log_format)
  logger = logging.getLogger(__name__)

  main(logger)
