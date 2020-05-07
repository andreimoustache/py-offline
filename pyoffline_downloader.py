import requests
from pyoffline_models import Resource


def download_resource(resource: Resource):
  print(f'Requesting {resource.url}.')
  response = requests.get(resource.url)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  resource.mimeType = response.headers["Content-Type"]
  resource.encoding = response.encoding
  resource.body = response.text

  return resource


def download_document(url, name):
  print(f'Requesting {url}.')
  response = requests.get(url)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (name, response.text, response.encoding)
