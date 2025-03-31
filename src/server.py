import socket

from .parser import parse_frame
from .handler import ConnectionHandler
from .constants import HOST, PORT, BUFFER_SIZE

class Server:
  def __init__(self):
    self.sock = None
    self.handler = ConnectionHandler()

  def start(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with self.sock:
      self.sock.bind((HOST, PORT))
      self.sock.listen()

      while True:
        connection, client_address = self.sock.accept()
        print(f"Client connection created with {client_address}")
        self.handle_connection(connection)

  def handle_connection(self, connection):
    buffer = b""

    with connection:
      while True:
        data = connection.recv(BUFFER_SIZE)

        if not data:
          break

        buffer += data
        print(f"buffer: {buffer}, data: {data}")

        frame, size = parse_frame(buffer)
        
        if frame:
          print(f"handle_connection frame: {frame}, size: {size}")
          response = self.handler.handle(frame)
          connection.sendall(response)

