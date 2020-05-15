from urllib.parse import urlparse
from pathlib import Path

class ConfigException(Exception):
  def __init__(self, message):
    super().__init__(message)


class Config:
  def __init__(self, cfg: dict):
    self.site_url = cfg.get("PYOFF_URL", None)
    self.depth = int(cfg.get("PYOFF_DEPTH", 1))
    self.write_destination = cfg.get("PYOFF_DESTINATION", ".")

    scheme, domain, path, _, _, _ = urlparse(self.site_url)
    self.domain = domain
    self.site_root = f'{scheme}://{domain}/'

    self.write_path = Path(f'./{self.write_destination}/')

    if self.site_url is None:
      raise ConfigException("I need a URL, please set the PYOFF_URL environment variable.")

  def __str__(self):
    return ','.join([f'{key}={value}' for (key,value) in self.__dict__.items()])
