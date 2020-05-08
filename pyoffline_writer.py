from pathlib import PurePath
from os import environ, makedirs
from sys import exit
from pyoffline_models import Resource
from q_consumer import Consumer
import pickle


class Writer():
  def __init__(self, path, consumer: Consumer):
    self.path = path
    self.consumer = consumer
    self.consumer.set_callback(self.callback)


  def start_consuming(self):
    while True:
      self.consumer.run()


  def callback(self, body):
    resource = pickle.loads(body)
    print(" [x] Received %r" % resource.name)
    self.write_to_file(resource)


  def write_to_file(self, resource: Resource):
    filename = PurePath(self.path / resource.name)
    print(f'Writing file to {filename}.')
    makedirs(filename.parent, exist_ok=True)
    with open(filename, 'w', encoding=resource.encoding) as file:
      file.write(resource.body)


if __name__ == "__main__":
  write_destination = environ.get("PYOFF_DESTINATION", ".")
  queue_host = environ.get("PYOFF_Q_HOST", "q")
  queue_name = environ.get("PYOFF_Q_FILES", "files")

  try:
    consumer = Consumer(queue_host, queue_name)
    print('Successfully created consumer.')
  except:
    print('Failed to create consumer.')
    exit(1)

  w = Writer(write_destination, consumer)
  w.start_consuming()
