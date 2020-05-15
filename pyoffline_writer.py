from pathlib import PurePath
from os import makedirs
from logging import getLogger
from pyoffline_models import Resource


class Writer:
  def __init__(self, path: str):
    self.logger = getLogger()
    self.path = path

    makedirs(self.path, exist_ok=True)


  def write(self, resource: Resource):
    name = resource.name[1:]
    filename = PurePath(self.path / name)
    self.logger.info(f'Writing file to {filename}.')
    makedirs(filename.parent, exist_ok=True)
    with open(filename, 'w', encoding="utf-8") as file:
      file.write(resource.body)
