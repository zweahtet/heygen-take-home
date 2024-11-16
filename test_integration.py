import subprocess
import time
from client import VideoTranslationClient


# Integration test that spins up server and runs client to get status
def test_integration():
    """
    Integration test that starts the server and uses the client library to query the job status.
    """
    # Start the server
    server_process = subprocess.Popen(
        ["uvicorn", "server:app", "--host", "localhost", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)  # Allow time for server to start

    try:
        # Use the client library to query the status
        client = VideoTranslationClient(base_url="http://localhost:8000")
        status = client.get_status()
        assert status in ["completed", "error", "unknown"]
    finally:
        server_process.terminate()
