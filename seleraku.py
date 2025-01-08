import urlparse
import json
import time
import requests
from loguru import logger
from requests.exceptions import RequestException

# Fungsi sinkron untuk menggantikan fungsi async
def call_api(url, data, token, proxy=None, timeout=60):
    headers = {
        "Authorization": "Bearer {}".format(token),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json",
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, json=data, headers=headers, proxies=proxies, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error("Error during API call: {}".format(e))
    except ValueError:
        logger.error("Failed to decode JSON response.")
    return None

# Fungsi sinkron untuk ping
def start_ping(token, ping_interval):
    while True:
        try:
            url = "https://nw.nodepay.org/api/network/ping"
            data = {"id": token, "timestamp": int(time.time())}
            response = call_api(url, data, token)
            if response:
                logger.info("Ping successful.")
            else:
                logger.warning("Ping failed.")
        except Exception as e:
            logger.error("Unexpected error: {}".format(e))
        time.sleep(ping_interval)

# Contoh penggunaan
if __name__ == "__main__":
    token = "your-token"
    start_ping(token, 2)
