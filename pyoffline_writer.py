from pathlib import PurePath
from os import makedirs


def write_to_file(path, name, body, encoding):
  filename = PurePath(path / name)
  print(f'Writing file to {filename}.')
  makedirs(filename.parent, exist_ok=True)
  with open(filename, 'w', encoding=encoding) as file:
    file.write(body)
