import threading

from config import Config


class FastReadCounter:
    def __init__(self, config: Config):
        self.config = config
        self.value = self.load(0)
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1
            if self.value % 10000 == 0:
                threading.Thread(target=self.dump).start()

        return self.value

    def dump(self):
        with open(self.config.counter, "w") as f:
            f.write(str(self.value))

        print("success dump counter")

    def load(self, default=0):
        if self.config.counter.exists():
            with open(self.config.counter, "r") as f:
                return int(f.read().splitlines()[0])

        return default
