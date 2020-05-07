from pathlib import PurePath
from os import makedirs
from pyoffline_models import Resource


def write_to_file(path, resource: Resource):
  filename = PurePath(path / resource.name)
  print(f'Writing file to {filename}.')
  makedirs(filename.parent, exist_ok=True)
  with open(filename, 'w', encoding=resource.encoding) as file:
    file.write(resource.body)
