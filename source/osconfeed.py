import json
import os
import warnings
from urllib.request import urlopen

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/app.json'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {URL} to {JSON}'
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)


if __name__ == '__main__':
    load()
