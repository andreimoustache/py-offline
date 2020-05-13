from logging import getLogger
from pika import BasicProperties, ConnectionParameters, SelectConnection, URLParameters


class Consumer():
  def __init__(self, q_host, q_port, queue_name, message_handler=None):
    self.queue_name = queue_name
    self.url = f'amqp://guest:guest@{q_host}:{q_port}/'
    self.connection = None
    self.channel = None
    self.consumer_tag = None
    self.publish_properties = BasicProperties(delivery_mode=2)
    self.message_handler = message_handler

    self.logger = getLogger(__name__)
    self.logger.info(f'Created QConsumer on {self.url} for topic {queue_name}.')


  def connect(self):
    return SelectConnection(URLParameters(self.url),
                            on_open_callback=self.on_connection_open,
                            on_open_error_callback=self.on_connection_open_error,
                            on_close_callback=self.on_connection_closed)


  def on_connection_open(self, unused_connection):
    self.logger.info("Connection opened.")
    self.connection.channel(on_open_callback=self.on_channel_open)


  def on_channel_open(self, channel):
    self.logger.info("Channel opened.")
    self.channel = channel
    self.channel.add_on_close_callback(self.on_channel_closed)
    self.channel.queue_declare(queue=self.queue_name, durable=True)
    self.channel.basic_qos(prefetch_count=1, callback=self.on_basic_qos_ok)


  def on_basic_qos_ok(self, _):
    self.consumer_tag = self.channel.basic_consume(self.queue_name, self.on_message)


  def on_channel_closed(self, channel, reason):
    self.logger.warning(f'Channel {channel} was closed: {reason}.')
    self.channel = None
    self.connection.close()


  def on_connection_open_error(self, unused_connection, err):
    self.logger.error('Connection open failed, retrying in 5s. %s', err)
    self.connection.ioloop.call_later(5, self.connection.ioloop.stop)


  def on_connection_closed(self, connection, reason):
    self.logger.info("Connection closed.", reason)


  def on_message(self, ch, method, properties, body):
    self.logger.debug("Received message.")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    self.message_handler(body)


  def set_message_handler(self, handler):
    self.message_handler = handler


  def run(self):
    try:
      self.connection = self.connect()
      self.connection.ioloop.start()
    except:
      self.logger.error('Error occured running consumer.', exc_info=True)
      self.stop()
      if (self.connection is not None and not self.connection.is_closed):
        self.connection.ioloop.start()
      self.logger.info('Stopped QConsumer.')

      raise


  def stop(self):
    self.logger.info('Stopping QConsumer.')
    if self.channel is not None:
      self.channel.close()
    if self.connection is not None:
      self.connection.close()

