import requests


def download_document(site_root, path):
  print(f'Requesting {site_root + path}.')
  response = requests.get(site_root + path)
  print(f'Got HTTP {response.status_code}, {response.headers["Content-Type"]}.')

  return (path, response.text, response.encoding)
