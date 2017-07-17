#!/usr/bin/env python

import json
import requests
import sys

from pprint import pprint
from urllib.parse import urljoin


def get_jwt(base_url, config):
    full_url = urljoin(base_url, "/users/authenticate/")
    headers = {'Content-type': 'application/json'}
    response = requests.post(
        full_url,
        headers=headers,
        data=json.dumps({'data': config}))
    return response.json()['data']['token']


def main():
    config = json.load(open(sys.argv[1]))
    base_url = config['base_url']
    token = get_jwt(base_url, config)
    full_url = urljoin(base_url, sys.argv[2])
    response = requests.get(
        full_url,
        headers={"Authorization": "Bearer {}".format(token)},
    )
    pprint(response.json())


if __name__ == '__main__':
    main()
