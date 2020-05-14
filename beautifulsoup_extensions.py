from url_extensions import is_own_url
from bs4 import Tag


def has_href_with_url(site_root: str):
  """Returns a function that checks whether a Beautifulsoup `Tag` has a
  `href` attribute pointing to the same domain as `site_root`
  """
  def f(tag: Tag):
    if not tag.has_attr("href"):
      return False

    if not is_own_url(site_root, tag["href"]):
      return False
    
    return True
  
  return f


def has_src_with_url(site_root):
  """Returns a function that checks whether a Beautifulsoup `Tag` has a
  `src` attribute pointing to the same domain as `site_root`
  """
  def f(tag: Tag):
    if not tag.has_attr("src"):
      return False

    if not is_own_url(site_root, tag["src"]):
      return False
    
    return True
  
  return f
