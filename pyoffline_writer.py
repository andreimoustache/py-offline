import logging
from pathlib import Path, PurePath
from threading import Thread
from os import environ, makedirs
from sys import exc_info, exit
from pyoffline_models import Resource
from q_consumer import Consumer
import pickle


class Writer():
  def __init__(self, path, consumer: Consumer):
    self.path = path
    self.consumer = consumer
    self.consumer.set_message_handler(self.callback)


  def run(self):
    consumer_thread = Thread(target=self.consumer.run, daemon=False)
    consumer_thread.start()


  def callback(self, body):
    resource = Resource.from_serialised(body)
    if type(resource) is not Resource:
      print("Received message in a wrong format.")
      return

    print(" [x] Received %r" % resource.name)
    self.write_to_file(resource)


  def write_to_file(self, resource: Resource):
    filename = PurePath(self.path / resource.name)
    print(f'Writing file to {filename}.')
    makedirs(filename.parent, exist_ok=True)
    with open(filename, 'w', encoding=resource.encoding) as file:
      file.write(resource.body)


if __name__ == "__main__":
  log_format = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                  '-35s %(lineno) -5d: %(message)s')
  logging.basicConfig(level=logging.INFO, format=log_format)
  logger = logging.getLogger(__name__)

  write_destination = environ.get("PYOFF_DESTINATION", "")
  queue_host = environ.get("PYOFF_Q_HOST", "q")
  queue_port = environ.get("PYOFF_Q_PORT", "5672")
  queue_name = environ.get("PYOFF_Q_FILES", "files")

  try:
    consumer = Consumer(queue_host, queue_port, queue_name)
    logger.info('Successfully created consumer.')
  except:
    logger.error('Failed to create consumer.', exc_info=True)
    exit(1)

  write_destination = Path(f'./{write_destination}/')
  w = Writer(write_destination, consumer)
  w.run()
