#
# Pull the latest arXiv papers for a given search term and write them to a markdown file.
#
# NOTE: arXiv asks that folks consider their financial limitations and miminize server load.
#       Don't send more than 3 requests per second.
#

import logging
import requests
from time import time
from xml.etree import ElementTree as ET


# get search term
query = input("Whatcha wanna lookup? ")
print("\n\n\n")

# log output to file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("log-%s-%s.md" % (query, time())),
        logging.StreamHandler()
    ]
)

# URL of the XML object
url = "https://export.arxiv.org/api/query?search_query=all:%s&sortBy=lastUpdatedDate&sortOrder=descending&max_results=5" % query.lower().replace(' ','%20')

# Send a GET request to the URL
response = requests.get(url)

# Parse the XML response
root = ET.fromstring(response.content)

# Namespace dictionary to find elements
namespaces = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

# Iterate over each entry in the XML data
for entry in root.findall('atom:entry', namespaces):
    # Extract and write the title
    title = entry.find('atom:title', namespaces).text
    title = ' '.join(title.split())  # Replace newlines and superfluous whitespace with a single space
    logging.info(f"# {title}\n")

    # Extract and write the published date and updated date
    published = entry.find('atom:published', namespaces).text
    updated = entry.find('atom:updated', namespaces).text
    # Determine if published and updated dates are the same
    if published == updated:
        logging.info(f"Published: {published}\n")
    else:
        logging.info(f"Published: {published}\nUpdated: {updated}\n")

    # Extract and write the link to the paper
    id = entry.find('atom:id', namespaces).text
    logging.info(f"[Link to the paper]({id})\n")

    # Extract and write the authors
    authors = entry.findall('atom:author', namespaces)
    logging.info("## Authors\n")
    for author in authors:
        name = author.find('atom:name', namespaces).text
        logging.info(f"- {name}")
    logging.info("\n")

    # Extract and write the summary
    summary = entry.find('atom:summary', namespaces).text
    logging.info(f"## Summary\n{summary}\n\n")
