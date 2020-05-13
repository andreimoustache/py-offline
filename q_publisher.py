from logging import getLogger
from sys import exc_info
from pika import BasicProperties, SelectConnection, ConnectionParameters, URLParameters


class Publisher():
  def __init__(self, q_host, q_port, queue_name):
    self.queue_name = queue_name
    self.url = f'amqp://guest:guest@{q_host}:{q_port}/'
    self.connection = None
    self.channel = None
    self.publish_properties = BasicProperties(delivery_mode=2)

    self.logger = getLogger(__name__)
    self.logger.info(f'Created QPublisher on {self.url} for topic {queue_name}.')


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


  def on_channel_closed(self, channel, reason):
    self.logger.warning(f'Channel {channel} was closed: {reason}.')
    self.channel = None
    self.connection.close()


  def on_connection_open_error(self, unused_connection, err):
    self.logger.error('Connection open failed. %s', err)
    raise


  def on_connection_closed(self, connection, reason):
    self.logger.info("Connection closed.", reason)


  def publish(self, key, message):
    self.logger.info("Publishing message")
    try:
      self.channel.basic_publish(
        body=message,
        properties=self.publish_properties,
        exchange="",
        routing_key=key
      )
      self.logger.debug(f'Published message size={len(message)} on queue={self.queue_name}.')
    except:
      self.logger.error(f'Error publishing message key={key}', exc_info=True)


  def run(self):
    try:
      self.connection = self.connect()
      self.connection.ioloop.start()
    except KeyboardInterrupt:
      self.logger.error('Error occured running publisher.', exc_info=True)
      self.stop()
      if (self.connection is not None and not self.connection.is_closed):
        self.connection.ioloop.start()
      self.logger.info('Stopped QPublisher.')

      raise


  def stop(self):
    self.logger.info('Stopping QPublisher.')
    if self.channel is not None:
      self.channel.close()
    if self.connection is not None:
      self.connection.close()
