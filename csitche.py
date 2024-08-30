import argparse
import os
import json
import sys
from services.scrapper import scrape, buildScrapeDict

def scrape_progress(links: set, external: set, finished: bool) -> any:
    if finished:
        yield buildScrapeDict(links, external)
    else:
        yield({'count' : len(links)})

if __name__=="__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Web Scraper CLI")
    parser.add_argument("function_name", choices=["scrape"], help="Function to execute")
    parser.add_argument("-u", "--url", required=True, help="URL to scrape")
    parser.add_argument("--limit", required=False, help="Max number of URL scrape", default=0)
    parser.add_argument("-o", "--output", required=True, help="Output file to save scraped URLs")
    args = parser.parse_args()

    if args.function_name == "scrape":
        results = {}
        for progress_update in scrape(args.url, int(args.limit), scrape_progress):
            if 'count' in progress_update :
                print(f"Progress: {progress_update['count']} links scraped.", end='\r')
            else:
                results  = progress_update
        print("\nScraping completed!")
        try:
            with open(args.output, 'w') as fp:
                json.dump(results, fp)
        except:
            print('Failed to write file.')
            print(results)