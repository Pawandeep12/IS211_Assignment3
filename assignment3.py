import argparse
import csv
import urllib.request
import re
from collections import Counter
from datetime import datetime


def download_file(url):
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    return content.splitlines()


def process_csv(data):

    rows = []
    for line in csv.reader(data):
        path, date_str, browser, status, size = line
        rows.append({
            'path': path,
            'datetime': date_str, 
            'browser': browser,
            'status': int(status),
            'size': int(size)
        })
    return rows



def find_image_hits(rows):
    
    image_pattern = re.compile(r".*\.(jpg|gif|png)$", re.IGNORECASE)
    total_hits = len(rows)
    image_hits = [row for row in rows if image_pattern.match(row['path'])]
    image_hit_percentage = (len(image_hits) / total_hits) * 100 if total_hits else 0
    print(f"Image requests account for {image_hit_percentage:.1f}% of all requests.")
    return image_hits



def find_most_popular_browser(rows):
    """Finds the most popular browser (Firefox, Chrome, IE, Safari)."""
    browser_counts = Counter()
    browser_patterns = {
        'Firefox': re.compile(r'Firefox', re.IGNORECASE),
        'Chrome': re.compile(r'Chrome', re.IGNORECASE),
        'Internet Explorer': re.compile(r'MSIE|Trident', re.IGNORECASE),
        'Safari': re.compile(r'Safari', re.IGNORECASE),
    }

    for row in rows:
        for browser, pattern in browser_patterns.items():
            if pattern.search(row['browser']):
                browser_counts[browser] += 1
                break

    most_common_browser = browser_counts.most_common(1)
    if most_common_browser:
        print(f"The most popular browser is {most_common_browser[0][0]} with {most_common_browser[0][1]} hits.")
    else:
        print("No browser data found.")

def count_hits_by_hour(rows):
    
    hour_counts = Counter()
    for i in range(0, 24):
        hour_counts[i] = 0
    
    for row in rows:
        try:
            date_obj = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')  # Parse the datetime string
            hour = date_obj.hour  # Extract the hour
            hour_counts[hour] += 1
        except ValueError:
            print(f"Error parsing date: {row['datetime']}")

    
    for hour, count in sorted(hour_counts.items()):
        print(f"Hour {hour:02d} has {count} hits.")



def main(url):
    print(f"Running main with URL = {url}...")

  
    data = download_file(url)

    
    rows = process_csv(data)

   
    find_image_hits(rows)

    
    find_most_popular_browser(rows)

    
    count_hits_by_hour(rows)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
