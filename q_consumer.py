from datetime import datetime, timedelta
from pika import BlockingConnection, ConnectionParameters


class Consumer():
  def __init__(self, host, queue_name, timeout=10):
    self.connection = BlockingConnection(ConnectionParameters(host=host))
    self.channel = self.connection.channel()
    self.queue_name = queue_name

    self.channel.queue_declare(queue=queue_name, durable=True)

    self.channel.basic_qos(prefetch_count=1)

    self.timeout =timedelta(seconds=timeout)
    self.last_received_at = datetime.now()


  def set_callback(self, callback):
    self.callback = callback
    self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message)


  def on_message(self, ch, method, properties, body):
    self.last_received_at = datetime.now()
    print("Received message.")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    self.callback(body)


  def is_timedout(self):
    return (datetime.now() - self.last_received_at) > self.timeout


  def run(self):
    self.channel.start_consuming()
