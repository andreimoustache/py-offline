from dataclasses import dataclass


@dataclass
class Resource:
  url: str
  name: str = ''
  mimeType: str = ''
  body: str = ''
  encoding: str = ''

@dataclass
class Document(Resource):
  depth: int = 1
