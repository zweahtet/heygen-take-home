# Video Translation Client Library
This is a simple client library to query the status of a video translation job.

## Installation
1. Create a Python virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Run the server:

```sh
uvicorn server:app --reload
```

## Usage
Create an instance of `VideoTranslationClient` with the base URL of the server and call the `get_status()` method to get the status of a video translation job.

```python
from client import VideoTranslationClient

client = VideoTranslationClient(base_url="http://localhost:8000")
status = client.get_status()
print(f"Final status: {status}")
```

Run the client script in a separate terminal to see the status of the video translation job:

```sh
python client.py
```

Example output:

```sh
INFO:VideoTranslationClient:Attempt 1: Job is still pending, retrying after 1 seconds.
INFO:VideoTranslationClient:Job completed after 2 attempts.
Final status: completed
```

## Testing
Run the integration tests using `pytest`:

```sh
pytest -s --log-cli-level=INFO test_integration.py
```

### Bells and Whistles
- **Adaptive Polling** with exponential backoff
- **Error Handling & Retries**
- **Logging** for tracking and debugging
- **Integration Testing** to validate the library behavior in real-world scenarios