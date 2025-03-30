import pytest

from src.parser import parse_frame
from src.data_types import SimpleString, Error, Integer, BulkString, Null, Array

# def test_parse_frame_simple_string_partial():
#   buffer = b"+part"
#   frame, frame_size = parse_frame(buffer)
#   assert frame is None
#   assert frame_size == 0


# def test_parse_frame_simple_string_full():
#   buffer = b"+OK\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == SimpleString("OK")
#   assert frame_size == 5


# def test_parse_error():
#   buffer = b"-Err\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == Error("Err")
#   assert frame_size == 6


# def test_parse_integer():
#   buffer = b":123\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == Integer(123)
#   assert frame_size == 6


# def test_parse_null():
#   buffer = b"_\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == Null()
#   assert frame_size == 3


# def test_parse_bulk_string():
#   buffer = b"$11\r\nhello world\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == BulkString("hello world", length=11)
#   assert frame_size == 18


# def test_parse_array_strings():
#   buffer = b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
#   frame, frame_size = parse_frame(buffer)
#   assert frame == Array([BulkString("hello", 5), BulkString("world", 5)], length=2)
#   assert frame_size == 26


@pytest.mark.parametrize("buffer,expected", [
  (b"+part", (None, 0)),
  (b"+OK\r\n", (SimpleString("OK"), 5)),
  (b"+OK\r\n+part", (SimpleString("OK"), 5)),
  (b"-Err\r\n", (Error("Err"), 6)),
  (b":123\r\n", (Integer(123), 6)),
  (b"_\r\n", (Null(), 3)),
  (b"$11\r\nhello world\r\n", (BulkString("hello world", length=11), 18)),
  (b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n", (Array([BulkString("hello", 5), BulkString("world", 5)], length=2), 26)),
])

def test_parse_frame(buffer, expected):
  got = parse_frame(buffer)
  assert got == expected