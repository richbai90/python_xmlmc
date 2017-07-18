import requests
from parser import Response


class EspSession:
    def __init__(self, server='127.0.0.1', port='5015'):
        self.server = server
        self.port = port
        self.token = None
        self.last_error = None
        self.last_response = None
        self._ensure_endpoint(server, port)
        self.session = requests.Session()
        self.session.headers.update({'Connection': 'close',
                                     'Cache-Control': 'no-cache',
                                     'Accept': 'text/xmlmc',
                                     'Content-Type': 'text/xmlmc; charset=UTF-8'
                                     })

    def _ensure_endpoint(self, server, port):
        self.endpoint = 'http://' + server + ':' + port

    def request(self, method_call):
        cookies = self.session.cookies.get_dict()
        headers = {'Content-Length': str(method_call.length),
                   'cookie': 'ESPSessionState=' + self.session.cookies.get('ESPSessionState') if cookies else ''}
        return Response(self.session.post(self.endpoint, method_call.tostring(), headers=headers).text.encode('utf-8'))
