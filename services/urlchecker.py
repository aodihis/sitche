import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url):
    try:
        req = requests.get(url)
        return (
            {
                'url' : url,
                'status_code': req.status_code,
                'redirect_url': req.url if req.url != url else '',
                'error' : None
            }
        )
    except requests.exceptions.RequestException as e:
         return {
                'url' : url,
                'status_code': '',
                'redirect_url':'',
                'error' : str(e)
            }
        


def check(urls):
    results = []
    with ThreadPoolExecutor(max_workers=3) as exc:
        futures = [exc.submit(fetch_url, url) for url in urls]
        for future in futures:
            results.append(future.result())
    return results