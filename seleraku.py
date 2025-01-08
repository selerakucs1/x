import urlparse
import json
import time
import requests
import logging
from requests.exceptions import RequestException

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Fungsi sinkron untuk menggantikan fungsi async
def call_api(url, data=None, proxy=None, timeout=60):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA2NDk2MTQzODY5MzQ1NzkyIiwiaWF0IjoxNzM1ODA2NTYxLCJleHAiOjE3MzcwMTYxNjF9.jjqHDHIXLfZE6PLWcqvG43ikgZWZqHss7KakrT6V9ubsRuxUsWz9rCP6_dd9LFBXmFVq3IoVQiMu4zXECaCj7g",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json",
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        # Pastikan data tidak None sebelum di-serialize
        json_data = json.dumps(data) if data else None
        response = requests.post(url, data=json_data, headers=headers, proxies=proxies, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error("Error during API call: {}".format(e))
    except ValueError:
        logger.error("Failed to decode JSON response.")
    return None

# Fungsi sinkron untuk ping
def start_ping(ping_interval):
    while True:
        try:
            url = "https://nw.nodepay.org/api/network/ping"
            # Data dikirim sesuai API
            data = {"timestamp": int(time.time())}
            response = call_api(url, data=data, proxy=None, timeout=60)
            if response:
                logger.info("Ping successful.")
            else:
                logger.warning("Ping failed.")
        except Exception as e:
            logger.error("Unexpected error: {}".format(e))
        time.sleep(ping_interval)

# Contoh penggunaan
if __name__ == "__main__":
    start_ping(2)
