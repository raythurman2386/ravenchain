import requests
import time
from datetime import datetime


def test_rate_limit():
    """
    Test the rate limiting on the health endpoint.
    The endpoint is limited to 5 requests per minute.
    """
    base_url = "http://localhost:8000/api/health"
    num_requests = 7

    print("\nTesting rate limiting on health endpoint...")
    print(f"Making {num_requests} requests (limit is 5 per minute)")
    print("-" * 50)

    for i in range(num_requests):
        timestamp = datetime.now().strftime("%H:%M:%S")
        try:
            response = requests.get(base_url)
            status_code = response.status_code

            if status_code == 200:
                print(f"[{timestamp}] Request {i + 1}: Success (Status: {status_code})")
            else:
                print(f"[{timestamp}] Request {i + 1}: Rate limit exceeded (Status: {status_code})")

        except requests.exceptions.RequestException as e:
            print(f"[{timestamp}] Request {i + 1}: Error - {str(e)}")

        time.sleep(0.5)


if __name__ == "__main__":
    test_rate_limit()
