import base64
from os.path import basename
from time import sleep

from requests import get, post
from json import dumps

import config


def docx_to_pdf_by_api(src: str, dist: str):
    if not config.secret_data:
        raise Exception("Api key not found")
    with open(src, 'br') as f:
        resp = post('https://api.convertio.co/convert', dumps({
            "apikey": config.CONVERTIO_API_KEY,
            "input": "base64",
            "file": str(base64.b64encode(f.read()))[2:-1],
            "filename": basename(src),
            "outputformat": "pdf",
        }))
    if resp.status_code < 400:
        conversion_id = resp.json()['data']['id']
        while True:
            sleep(1)
            resp = get(f'https://api.convertio.co/convert/{conversion_id}/status')
            if resp.status_code < 400:
                resp = resp.json()
                if resp['data']['step'] == 'finish':
                    url = resp['data']['output']['url']
                    resp = get(url)
                    if resp.ok:
                        with open(dist, 'wb') as f:
                            f.write(resp.content)
                        break
                    raise Exception(f"Cannot upload file:\n{resp.text}")
            else:
                raise Exception(resp.text)
