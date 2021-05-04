import unittest

from config import Config
from crawler import Crawler
from utils.counter import FastReadCounter
from utils.filter import BloomFilter


class TestSearchEngine(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSearchEngine, self).__init__(*args, **kwargs)
        self.config = Config("dev")

    def test_counter(self):
        self.config.counter.unlink(missing_ok=True)

        counter = FastReadCounter(self.config)
        self.assertEqual(1, counter.increment())
        self.assertEqual(2, counter.increment())
        counter.dump()
        counter = FastReadCounter(self.config)
        self.assertEqual(3, counter.increment())

    def test_bloom_filter(self):
        self.config.crawler.bloom_filter.unlink(missing_ok=True)
        bloom_filter = BloomFilter(self.config)
        url = self.config.crawler.seed_url
        self.assertFalse(bloom_filter.get(url))
        bloom_filter.set(url)
        self.assertTrue(bloom_filter.get(url))

        bloom_filter.dump()
        bloom_filter = BloomFilter(self.config)
        self.assertTrue(bloom_filter.get(url))

    def test_crawler(self):
        self.config.crawler.linksA.unlink(missing_ok=True)
        self.config.crawler.linksB.unlink(missing_ok=True)
        self.config.crawler.doc_id_mapping.unlink(missing_ok=True)
        self.config.crawler.doc_raw.unlink(missing_ok=True)
        self.config.crawler.bloom_filter.unlink(missing_ok=True)
        self.config.counter.unlink(missing_ok=True)

        crawler = Crawler(self.config)
        crawler.fetch()

        with open(self.config.crawler.doc_id_mapping, "r") as f:
            lines = f.read().splitlines()
            [id, u] = lines[0].split("\t")
            self.assertEqual(id, "1")
            self.assertEqual(u, self.config.crawler.seed_url)

        with open(self.config.crawler.linksB, "r") as f:
            lines = f.read().splitlines()
            self.assertTrue(len(lines) > 10)

        with open(self.config.crawler.linksA, "r") as f:
            lines = f.read().splitlines()
            self.assertTrue(len(lines) == 0)

        with open(self.config.crawler.doc_raw, "r") as f:
            lines = f.read().splitlines()
            [id, size, content] = lines[0].split("\t")
            self.assertEquals("1", id)
            self.assertTrue(len(content) > 0)

        crawler.fetch()

        with open(self.config.crawler.linksA, "r") as f:
            lines = f.read().splitlines()
            self.assertTrue(len(lines) > 10)

        crawler.bloom_filter.dump()


if __name__ == '__main__':
    unittest.main()
