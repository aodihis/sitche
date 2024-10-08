import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from typing import Set, Tuple, Callable, Optional

def scrape(url: str, limit: int = 0, generator_callback: Optional[Callable[[Set, Set, Set, bool], None]] = None) -> any:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
    source = urlparse(url)
    links_stack, links, external, brokenLinks = [url], set([url]), set(), set()
    while links_stack:
        vlink = links_stack.pop()
        try:
            response = requests.get(vlink, headers=headers)
            if response.status_code == 404:
                brokenLinks.add(vlink)
                links.remove(vlink)
                continue
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
            else:
                external.add(link['href'].strip())
            if generator_callback:
                yield from generator_callback(links, external, brokenLinks, False)
            if limit and len(links) >= limit:
                break
        if limit and len(links) >= limit:
            break
    
    if generator_callback:
        yield from generator_callback(links, external, brokenLinks, True)
    else:
        return buildScrapeDict(links, external, brokenLinks)


def buildScrapeDict(internalLinks:set[str], externalLinks:set[str], brokenLinks: set[str]):
    data = {
        'links':[],
        'external': [],
        'brokenLinks' : []
    }
    for link in internalLinks:
        data['links'].append(link)
    for link in externalLinks:
        data['external'].append(link)
    for link in brokenLinks:
        data['brokenLinks'].append(link)
    return data

