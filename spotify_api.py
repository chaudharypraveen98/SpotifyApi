import base64
import requests
import datetime
from urllib.parse import urlencode

client_id = 'Enter your Client id'
client_key = 'Enter you Cliend key'


class SpotifyApi(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expires = True
    client_id = None
    client_key = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_key = client_key

    def get_token_header(self):
        cred_base64 = self.get_client_credentials()
        return {
            "Authorization": f'Basic {cred_base64}'
        }

    def get_client_credentials(self):
        client_id = self.client_id
        client_key = self.client_key
        if client_key == None or client_key == None:
            raise Exception("you must set the client credentials")
        cred = f'{client_id}:{client_key}'
        cred_base64 = base64.b64encode(cred.encode())
        return cred_base64.decode()

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        if r.status_code not in range(200, 299):
            return False
        token_response_data = r.json()
        now = datetime.datetime.now()
        expires_in = token_response_data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expires = expires < now
        self.access_token = token_response_data['access_token']
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def base_search(self, query_params):
        header = self.get_resource_header()
        endpoint = 'https://api.spotify.com/v1/search'
        lookup_url = f'{endpoint}?{query_params}'
        r = requests.get(lookup_url, headers=header)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query, operator=None, operator_query=None, search_type="artist"):
        if query is None:
            raise Exception("a query is required")
        if isinstance(query, dict):
            query = " ".join([f'{k}:{v}' for k, v in query.items()])
        if operator is not None and operator_query is not None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f'{query} {operator} {operator_query}'

        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

    def get_resource_header(self):
        access_token = self.get_access_token()
        header = {
            "Authorization": f'Bearer {access_token}'
        }
        return header

    def get_resource(self, lookup_id, resourse_type='albums', version='v1'):
        lookup_url = f"https://api.spotify.com/{version}/{resourse_type}/{lookup_id}"
        header = self.get_resource_header()
        r = requests.get(lookup_url, headers=header)
        return r.json()

    def get_album(self, lookup_id):
        return self.get_resource(lookup_id, resourse_type='albums')

    def get_artist(self, lookup_id):
        return self.get_resource(lookup_id, resourse_type='artists')