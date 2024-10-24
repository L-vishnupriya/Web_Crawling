from html.parser import HTMLParser
from urllib import parse
import logging

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    try:
                        url = parse.urljoin(self.base_url, value)
                        if url:
                            self.links.add(url)
                    except Exception as e:
                        logging.error(f"Error processing URL {self.page_url}: {e}")

    def page_links(self):
        return self.links

    def error(self, message):
        logging.error(f"HTML Parsing Error: {message}")
