import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from typing import Set, Tuple, Callable, Optional

def scrape(url: str, limit: int = 0, progress_callback: Optional[Callable[[int, str], None]] = None) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
    source = urlparse(url)
    links_stack, links, external = [url], set([url]), set()
    while links_stack:
        vlink = links_stack.pop()
        try:
            response = requests.get(vlink, headers=headers)
        except requests.exceptions.RequestException as e:
            continue
        for link in BeautifulSoup(response.content , 'html.parser', parse_only=SoupStrainer('a')):
            if not link.has_attr('href'):
                continue
            alink = urlparse(link['href'])
            if alink.netloc == '' or alink.netloc == source.netloc:
                if alink.netloc == '' and alink.path.startswith('/'):
                    nurl = url.rstrip('/') + (alink.path + '?' + alink.query if alink.query else alink.path)
                elif alink.netloc == '':
                    nurl = vlink.rstrip('/') + '/' + (alink.path + '?' + alink.query if alink.query else alink.path)
                else:
                    nurl = link['href'].strip()
                if nurl not in links and nurl.rstrip('/') not in links and nurl+'/' not in links:
                    links.add(nurl)
                    links_stack.append(nurl)
                    if progress_callback:
                        progress_callback(len(links), nurl)
            else:
                external.add(link['href'].strip())
            if limit and len(links) >= limit:
                break
        if limit and len(links) >= limit:
            break
    
    return buildScrapeDict(links, external)


def buildScrapeDict(internalLinks:list[str], externalLinks:list[str]):
    data = {}
    data['links'] = []
    data['external'] = []
    for link in internalLinks:
        data['links'].append(link)
    for link in externalLinks:
        data['links'].append(link)
    return data

