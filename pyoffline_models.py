from dataclasses import dataclass
from pickle import dumps, loads


@dataclass
class Resource:
  url: str
  name: str = ''
  mimeType: str = ''
  body: str = ''
  encoding: str = ''

  def to_serialised(self):
    return dumps(self)
  
  @staticmethod
  def from_serialised(serialised):
    return loads(serialised)

@dataclass
class Document(Resource):
  depth: int = 1
