from sys import exc_info
from pika import BasicProperties, BlockingConnection, ConnectionParameters


class Publisher():
  def __init__(self, host, queue_name):
    self.connection = BlockingConnection(ConnectionParameters(host=host))
    self.channel = self.connection.channel()

    self.channel.queue_declare(queue=queue_name, durable=True)
    self.properties = properties=BasicProperties(delivery_mode=2)


  def publish(self, key, message):
    print(f'Publishing message size={len(message)}.')
    try:
      self.channel.basic_publish(
        body=message,
        properties=self.properties,
        exchange="",
        routing_key=key
      )
    except:
      print(f'Error publishing message key={key}')
      print(exc_info()[0])
