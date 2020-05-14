from logging import getLogger
from pyoffline_models import Resource


class Downloader:
  def __init__(self, http_client):
    self.logger = getLogger()
    self.http_client = http_client


  def download(self, resource: Resource):
    self.logger.info(f'Requesting {resource.url}.')
    response = self.http_client.get(resource.url)
    self.logger.info(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

    resource.mimeType = response.headers["Content-Type"]
    resource.encoding = response.encoding
    resource.body = response.text

    return resource
