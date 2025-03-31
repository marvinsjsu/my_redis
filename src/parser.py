from .data_types import SimpleString, Error, Integer, Null, BulkString, Array


BIN_STR_DELIMITER = b"\r\n"
DELIMITER_LENGTH = 2

def parse_frame(buffer):
  has_bin_str_delimiter = buffer.find(BIN_STR_DELIMITER) != -1

  if has_bin_str_delimiter is False:
    return None, 0
  else:
    match chr(buffer[0]):
      case '+':
        delim = buffer.find(BIN_STR_DELIMITER)
        
        if delim != -1:
          return SimpleString(data=buffer[1:delim].decode()), delim + DELIMITER_LENGTH

      case '-':
        delim = buffer.find(BIN_STR_DELIMITER)
        
        if delim != -1:
          return Error(data=buffer[1:delim].decode()), delim + DELIMITER_LENGTH
        
      case ':':
        delim = buffer.find(BIN_STR_DELIMITER)

        if delim != -1:
          return Integer(data=int(buffer[1:delim].decode())), delim + DELIMITER_LENGTH
        
      case '_':
        delim = buffer.find(BIN_STR_DELIMITER)

        if delim != -1:
          return Null(), delim + DELIMITER_LENGTH

      case '$':
        first_delim = buffer.find(BIN_STR_DELIMITER)

        if first_delim == -1:
          return None, 0

        try:
          length = int(buffer[1:first_delim].decode())
        except ValueError:
          return None, 0

        total_needed = first_delim + DELIMITER_LENGTH + length + DELIMITER_LENGTH

        if len(buffer) < total_needed:
          return None, 0

        start_of_data = first_delim + DELIMITER_LENGTH
        end_of_data = start_of_data + length
        data = buffer[start_of_data:end_of_data].decode()

        return BulkString(data=data, length=length), total_needed

      case '*':
        first_delim = buffer.find(BIN_STR_DELIMITER)

        if first_delim == -1:
          return None, 0

        try:
          length = int(buffer[1:first_delim].decode())
        except ValueError:
          return None, 0

        array = []
        curr_start_of_data = first_delim + len(BIN_STR_DELIMITER)
        data = buffer[curr_start_of_data:]

        print(f"first_delim: {first_delim}, length: {length}, data: {data}")

        for _ in range(length):
          item, size = parse_frame(data)

          print(f"item: {item}, size: {size}")

          if item is None or size == 0:
            return None, 0 
          
          array.append(item)
          data = data[size:]
          curr_start_of_data += size

        print(f"array: {array}")

        return Array(data=array, length=length), curr_start_of_data

  return None, 0
