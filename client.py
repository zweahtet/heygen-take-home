import requests
import time
import logging

class VideoTranslationClient:
    """
    VideoTranslationClient is a client library for polling the status of a video translation job.

    This client library interacts with the video translation server's `/status` endpoint to retrieve the job status.
    It includes features like adaptive polling using an exponential backoff mechanism, retry handling for transient errors,
    and comprehensive logging to provide visibility into the polling process.

    ### Features:
    - **Adaptive Polling**: The polling frequency is managed with exponential backoff to reduce server load and optimize efficiency.
    - **Retry Handling**: If there are intermittent server errors, the client will retry with a delay.
    - **Logging**: Logs are provided for every polling attempt, which helps users understand the status and any issues encountered.

    ### Usage:
    1. Instantiate the `VideoTranslationClient` with the base URL of the video translation server.
    2. Call the `get_status()` method to retrieve the current job status.

    ### Example:
    ```python
    client = VideoTranslationClient(base_url="http://localhost:8000")
    status = client.get_status()
    print(f"Final status: {status}")
    ```
    """
    
    def __init__(self, base_url, max_attempts=10, backoff_factor=1.5, initial_delay=1):
        """
        Initialize the VideoTranslationClient.

        Args:
            base_url (str): The base URL of the video translation server.
            max_attempts (int): Maximum number of polling attempts.
            backoff_factor (float): Factor by which the delay increases after each attempt.
            initial_delay (int): Initial delay (in seconds) before polling the server.
        """
        self.base_url = base_url
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.logger = logging.getLogger("VideoTranslationClient")
        logging.basicConfig(level=logging.INFO)

    def get_status(self):
        """
        Poll the server to get the status of the video translation job.

        Uses exponential backoff to minimize server load and optimize polling frequency.

        Returns:
            str: The final status of the job, which can be "completed", "error", or "unknown".
        """
        delay = self.initial_delay
        for attempt in range(self.max_attempts):
            try:
                response = requests.get(f"{self.base_url}/status")
                response.raise_for_status()
                result = response.json().get("result")

                if result == "completed":
                    self.logger.info(f"Job completed after {attempt + 1} attempts.")
                    return "completed"
                elif result == "error":
                    self.logger.error("Job ended in error.")
                    return "error"
                else:
                    self.logger.info(
                        f"Attempt {attempt + 1}: Job is still pending, retrying after {delay} seconds."
                    )
                    time.sleep(delay)
                    delay *= self.backoff_factor
            except requests.RequestException as e:
                self.logger.error(
                    f"Attempt {attempt + 1}: Error occurred - {str(e)}. Retrying..."
                )
                time.sleep(delay)
                delay *= self.backoff_factor

        self.logger.error("Max attempts reached. Job status could not be determined.")
        return "unknown"


# Usage example
# Uncomment the following code to run the client library if you want to test it independently.
# Make sure the server is running before executing this code.
# if __name__ == "__main__":
#     client = VideoTranslationClient(base_url="http://localhost:8000")
#     status = client.get_status()
#     print(f"Final status: {status}")
