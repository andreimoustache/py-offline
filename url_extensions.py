from urllib.parse import urlparse


def is_own_url(site_root, url):
  """Checks whether `url` is part of the same domain as `site_root`.
  """
  scheme, domain, _, _, _, _ = urlparse(url)
  if scheme == "" and domain == "":
    return True
  else:
    return f'{scheme}://{domain}/' in [site_root, ""]


def make_url_absolute(site_root, url):
  """Returns an absolute url, with the base `site_root`.
  """
  scheme, domain, _, _, _, _ = urlparse(url)
  if scheme == "" and domain == "":
    return f'{site_root}/{url}'
  else:
    return url


def make_url_relative(site_root, url):
  """Returns a relative url, from the base `site_root`
  """
  _, _, path, _, _, _ = urlparse(url)
  return "/index.html" if path in ["/", ""] else path
