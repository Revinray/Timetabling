import subprocess
import requests
import time
from environment import NGROK_URL, NGROK_PORT

def is_ngrok_running():
    try:
        response = requests.get(NGROK_URL)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def start_ngrok():
    domain = NGROK_URL.split('//')[1]
    subprocess.Popen(['ngrok', 'http', '--domain', domain, str(NGROK_PORT)])
    time.sleep(5)  # Wait for ngrok to start

if __name__ == "__main__":
    if not is_ngrok_running():
        print("Ngrok is not running. Starting ngrok...")
        start_ngrok()
    else:
        print("Ngrok is already running.")