

class ConnectionHandler:
  def __init__(self):
    pass

  def handle(self, frame):
    print(f"frame: {frame.data[0].get_data()}")

    command = frame.data[0].get_data()

    print(f"command: {command}")

    match command:
      case 'PING':
        return b"+PONG\r\n"

      case 'ECHO':
        data = frame.data[1]
        return data.resp_encode()
      

      
