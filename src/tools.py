import requests

from tokens_config import TokenData

s = requests.Session()


def get_req(url, timeout=15):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36',
    }
    r = s.get(url, timeout=timeout, headers=headers)
    if r.status_code == 200:
        try:
            data = r.json()
            return {'ok': 1, 'data': data}
        except Exception as e:
            return {'ok': 0, 'info': f'Cant parse json from API: {url}\nError Info: {e}'}

    else:
        return {'ok': 0, 'info': f'Request status code "{r.status_code}"\nAPI:{url}'}


async def async_get_req(url, session, timeout=30, headers=None, method='get', json=None):
    if headers is None:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 Safari/537.36',
        }

    if method == 'get':

        async with session.get(url, timeout=timeout, headers=headers) as r:
            if r.status == 200:
                try:
                    data = await r.json()
                    return {'ok': 1, 'data': data}
                except Exception as e:
                    return {'ok': 0, 'info': f'Cant parse json from API: {url}\nError Info: {e}'}

            else:
                return {'ok': 0, 'info': f'Request status code "{r.status}"\nAPI:{url}'}

    else:
        async with session.post(url, timeout=timeout, headers=headers, json=json) as r:
            if r.status == 200:
                try:
                    data = await r.json()
                    return {'ok': 1, 'data': data}
                except Exception as e:
                    return {'ok': 0, 'info': f'Cant parse json from API: {url}\nError Info: {e}'}

            else:
                return {'ok': 0, 'info': f'Request status code "{r.status}"\nAPI:{url}'}