import requests


def download_resource(url, name):
  print(f'Requesting {url}.')
  response = requests.get(url)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (name, response.text, response.encoding)


def download_document(url, name):
  print(f'Requesting {url}.')
  response = requests.get(url)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (name, response.text, response.encoding)
