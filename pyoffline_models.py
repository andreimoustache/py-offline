from dataclasses import dataclass


@dataclass
class Resource:
  url: str
  name: str = ''
  mimeType: str = ''
  body: str = ''
  encoding: str = ''

  def __str__(self):
    return f'{type(self).__name__}(name={self.name})'


@dataclass
class Document(Resource):
  depth: int = 1

  def __str__(self):
    return f'{type(self).__name__}(name={self.name}, depth={self.depth})'
