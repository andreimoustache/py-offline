from urllib.parse import urlparse


def is_own_url(site_root, url):
  """Checks whether `url` is part of the same domain as `site_root`.
  """
  scheme, domain, _, _, _, _ = urlparse(url)
  return f'{scheme}://{domain}/' in [site_root, ""]
