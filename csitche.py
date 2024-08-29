import argparse
import os
import json
import sys
from services.scrapper import scrape

if __name__=="__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Web Scraper CLI")
    parser.add_argument("function_name", choices=["scrape"], help="Function to execute")
    parser.add_argument("-u", "--url", required=True, help="URL to scrape")
    parser.add_argument("-o", "--output", required=True, help="Output file to save scraped URLs")
    args = parser.parse_args()

    if args.function_name == "scrape":
        results = scrape(args.url, 100)
        try:
            with open(args.output, 'w') as fp:
                json.dump(results, fp)
        except:
            print('Failed to write file.')
            print(results)