import requests


def download_resource(url, name):
  print(f'Requesting {url}.')
  response = requests.get(url)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (name, response.text, response.encoding)


def download_document(site_root, path):
  print(f'Requesting {site_root + path}.')
  response = requests.get(site_root + path)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (path, response.text, response.encoding)
