"""Small authenticated clients; credentials stay out of arguments, URLs and errors."""
from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import uuid

USER_AGENT = 'TitanRelics-release/1.0 (https://github.com/Auda29/Titan-Relics)'
BASES = {'modrinth': 'https://api.modrinth.com/v2',
         'curseforge': 'https://minecraft.curseforge.com/api'}


def credential(platform):
    value = os.environ.get(platform.upper() + '_TOKEN', '').strip()
    if not value:
        path = Path.home() / '.config/titan-relics' / (platform + '.token')
        if path.is_file():
            value = path.read_text(encoding='utf-8').strip()
    if not value or any(c in value for c in '\r\n'):
        raise ValueError('Missing or invalid ' + platform + ' credential')
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected authenticated API redirect')


class Client:
    def __init__(self, platform):
        self.platform = platform
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, method='GET', data=None, content_type='application/json'):
        if not path.startswith('/') or path.startswith('//'):
            raise ValueError('Expected relative API path')
        headers = {'User-Agent': USER_AGENT, 'Accept': 'application/json',
                   'Authorization' if self.platform == 'modrinth' else 'X-Api-Token': credential(self.platform)}
        if data is not None:
            if not isinstance(data, bytes):
                data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = content_type
        request = urllib.request.Request(BASES[self.platform] + path, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=120) as response:
                raw = response.read()
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'{self.platform} API {method} failed: HTTP {error.code}') from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError(self.platform + ' API connection failed') from None
        return json.loads(raw) if raw else None

    def upload(self, path, metadata, file):
        boundary = 'TitanRelics' + uuid.uuid4().hex
        field = 'data' if self.platform == 'modrinth' else 'metadata'
        body = (f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"\r\n'
                'Content-Type: application/json\r\n\r\n').encode()
        body += json.dumps(metadata).encode('utf-8')
        body += (f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; '
                 f'filename="{file.name}"\r\nContent-Type: application/java-archive\r\n\r\n').encode()
        body += file.read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
        return self.request(path, 'POST', body, 'multipart/form-data; boundary=' + boundary)


def download(url):
    """Public file download, deliberately without API credentials."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.username or parsed.password:
        raise ValueError('Expected public HTTPS download URL')
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': USER_AGENT}), timeout=120) as response:
            return response.read()
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError('Public file download failed') from None
