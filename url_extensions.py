from urllib.parse import urlparse


def is_own_url(site_root, url):
  scheme, domain, _, _, _, _ = urlparse(url)
  return f'{scheme}://{domain}/' in [site_root, ""]
