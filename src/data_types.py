from dataclasses import dataclass
from typing import List, Union


@dataclass
class SimpleString:
  data: str

  def resp_encode(self):
    return f"+{self.data}\r\n".encode()


@dataclass
class Error:
  data: str

  def resp_encode(self):
    return f"-{self.data}\r\n".encode()

@dataclass
class Integer:
  data: int

  def resp_encode(self):
    return f":{self.data}\r\n".encode()


@dataclass
class Null:

  def resp_encode():
    return f"_\r\n".encode()


@dataclass
class BulkString:
  data: str | None
  length: int

  def resp_encode(self):
    if self.data is None:
      return f"$-1\r\n".encode()
    
    return f"${self.length}\r\n{self.data}\r\n".encode()


@dataclass
class Array:
  data: List[Union[SimpleString, Error, Integer, Null, BulkString]]
  length: int

  def resp_encode(self):    
    return f"*{self.length}\r\n{self.data}".encode()

