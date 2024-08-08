import requests

class ConnectionRequestsServices:
    def __init__(self):
        pass

    def check_connection_state(self, urlToCheck):
        try:
            response = requests.get(urlToCheck, timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException:
            return False