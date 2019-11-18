import requests
import json
import sys
import requests.packages.urllib3.exceptions
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RestApiCalls:
    """Class for REST API methods"""

    def __init__(self, vmanage_ip, username, password):
        """Initiates a new sdwan instance which represents new connection (login)
        to the SD-WAN controller"""

        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        """Login method - creates anew session to the SD-WAN controller """

        base_url_str = f'https://{vmanage_ip}:443/'
        login_action = '/j_security_check'
        login_data = {'j_username': username, 'j_password': password}
        login_url = base_url_str + login_action
        url = base_url_str + login_url
        sess = requests.session()
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b'<html>' in login_response.content:
            print("Login Failed")
            sys.exit(0)

        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        """GET Call"""

        url = f'https://{self.vmanage_ip}:443/dataservice/{mount_point}'
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content

        return data

    def post_request(self, mount_point: object, payload: object,
                     headers: object = {'Content-Type': 'application/json'}) -> object:

        """POST Call"""

        url = f'https://{self.vmanage_ip}:443/dataservice/{mount_point}'
        payload = json.dumps(payload)
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.json()

        return data

    def delete_request(self, mount_point, id):
        """DELETE Call"""

        url = f'https://{self.vmanage_ip}:443/dataservice/{mount_point} + {id}'
        response = self.session[self.vmanage_ip].delete(url=url, verify=False)
        data = response.content

        return data
