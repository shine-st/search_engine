import base64
import re
import traceback

import requests
from bs4 import BeautifulSoup

from config import Config
from utils.counter import FastReadCounter
from utils.filter import BloomFilter


def write(io, *contents):
    for i in range(len(contents)):
        c = contents[i] if isinstance(contents[i], str) else str(contents[i])
        io.write(c)
        if i < len(contents) - 1:
            io.write("\t")

    io.write("\n")
    io.flush()


class Crawler:
    def __init__(self, config: Config):

        if not config.crawler.linksA.exists():
            with open(config.crawler.linksA, "w") as f:
                f.write(config.crawler.seed_url)
                f.write("\n")

        self.read_links_path = config.crawler.linksA
        self.write_links_path = config.crawler.linksB
        self.prepare_links_io()

        self.doc_id_mapping_io = open(config.crawler.doc_id_mapping, "a")
        self.doc_raw_io = open(config.crawler.doc_raw, "a")

        self.counter = FastReadCounter(config)
        self.bloom_filter = BloomFilter(config)

        self.http_pattern = re.compile("^http")

    def prepare_links_io(self):
        self.read_links_io = open(self.read_links_path, "r+")
        self.candidate_pool = self.read_links_io.read().splitlines()[::-1]
        self.write_links_io = open(self.write_links_path, "a")

    def fetch(self):
        # todo: get url function
        url = self.candidate_pool.pop()

        try:
            if not self.bloom_filter.get(url):
                print("fetch url: " + url)

                self.bloom_filter.set(url)
                resp = requests.get(url)
                id = self.counter.increment()

                base64_content = base64.b64encode(resp.content).decode("utf-8")
                write(self.doc_raw_io, id, len(resp.content), base64_content)
                write(self.doc_id_mapping_io, id, url)

                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.findAll('a'):
                    href = a.get("href")
                    if self.http_pattern.match(href):
                        write(self.write_links_io, href)

        except Exception as inst:
            traceback.print_exc()

        if len(self.candidate_pool) == 0:
            self.read_links_io.truncate(0)
            self.read_links_io.close()
            self.write_links_io.close()
            self.read_links_path, self.write_links_path = self.write_links_path, self.read_links_path
            self.prepare_links_io()
