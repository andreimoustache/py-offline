from url_extensions import is_own_url


def has_href_with_own_url(site_root):
  def f(tag):
    if not tag.has_attr("href"):
      return False

    if not is_own_url(site_root, tag["href"]):
      return False
    
    return True
  
  return f


def has_src_with_own_url(site_root):
  def f(tag):
    if not tag.has_attr("src"):
      return False

    if not is_own_url(site_root, tag["src"]):
      return False
    
    return True
  
  return f
