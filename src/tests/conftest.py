import time
import threading

import pytest

import main


@pytest.fixture
def server(scope="module"):
    threading.Thread(target=main, daemon=True).start()
    time.sleep(0.1)  # 100ms
    yield
    # pyredis.shutdown()

    