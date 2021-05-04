import pickle
import threading
import time

import mmh3

from config import Config


class BloomFilter:
    def __init__(self, config: Config):
        self.config = config
        self.hash_funcs = [lambda x: mmh3.hash(x), lambda x: hash(x)]
        self.filter = self.load([0] * 312500)

        self.dump_trigger = time.time()

    def set(self, s: str):
        for f in self.hash_funcs:
            hv = abs(f(s))
            byte_index = hv % 312500
            bit_index = hv % 32

            self.filter[byte_index] |= (1 << bit_index)

        if time.time() - self.dump_trigger > 1800:
            threading.Thread(target=self.dump).start()
            self.dump_trigger = time.time()

    def get(self, s: str):
        for f in self.hash_funcs:
            hv = abs(f(s))
            byte_index = hv % 312500
            bit_index = hv % 32

            if (self.filter[byte_index] & 1 << bit_index) == 0:
                return False

        return True

    def dump(self):
        with open(self.config.crawler.bloom_filter, "wb") as f:
            pickle.dump(self.filter, f)
        print("success dump bloom_filter")

    def load(self, default=[0] * 312500):
        if self.config.crawler.bloom_filter.exists():
            with open(self.config.crawler.bloom_filter, "rb") as f:
                return pickle.load(f)

        return default
