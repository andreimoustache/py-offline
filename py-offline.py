from os import environ
from queue import Queue
from sys import version_info, exit
from threading import Thread
import logging
import requests
from config import Config, ConfigException
from pyoffline_writer import Writer
from pyoffline_parser import Parser
from pyoffline_downloader import Downloader
from pyoffline_models import Document, Resource
from queue_processors import processor, fork_processor
from url_extensions import make_url_relative


def process_site(config:Config,
                  urls: Queue,
                  resources: Queue,
                  files: Queue,
                  downloader:Downloader,
                  parser: Parser,
                  writer: Writer):

  first_path = make_url_relative(config.site_root, config.site_url)
  first_document = Document(config.site_url, name=first_path, depth=0)
  urls.put(first_document)

  downloader_args = (urls, downloader.download, resources)
  parser_args = (resources, parser.parse, parser.is_resource_writable, files, urls)
  writer_args = (files, writer.write)

  Thread(name="downloader", target=processor, args=downloader_args, daemon=True).start()
  Thread(name="parser", target=fork_processor, args=parser_args, daemon=True).start()
  Thread(name="writer", target=processor, args=writer_args, daemon=True).start()

  urls.join()
  resources.join()
  files.join()


def main(logger: logging.Logger):
  try:
    config = Config(environ)
  except ConfigException as ex:
    logger.fatal(ex.args)
    return exit(1)

  logger.info("Starting py-offline")
  logger.info(config)

  downloader = Downloader(requests)
  parser = Parser(config.site_root)
  writer = Writer(config.write_path)

  urls, resources, files = Queue(), Queue(), Queue()
  process_site(config, urls, resources, files, downloader, parser, writer)


if __name__ == "__main__":
  log_level = environ.get("LOGLEVEL", "INFO")
  log_format = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s [%(threadName)s] %(lineno) -5d: %(message)s')
  logging.basicConfig(level=log_level, format=log_format)
  logger = logging.getLogger(__name__)

  main(logger)
