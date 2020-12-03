import contextlib
import time


class Averager(object):
    def __init__(self):
        self.avg = 0
        self.count = 0

    def insert(self, value):
        self.avg = ((self.count * self.avg) + value) / float(self.count + 1)
        self.count += 1

    def value(self):
        return self.avg

    def __repr__(self):
        return str(self.value())


class RollingAverager(object):
    def __init__(self, window):
        self.window = window
        self.values = [None] * window
        self.count = 0

    def insert(self, value):
        i = self.count % self.window
        self.values[i] = value
        self.count += 1

    def value(self):
        ct = 0
        s = 0
        for v in self.values:
            if v is not None:
                s += v
                ct += 1
        return s / float(ct)

    def __repr__(self):
        return str(self.value())


class Stats(object):
    def __init__(self):
        self.data = {}

    def incr(self, key):
        if key not in self.data:
            self.data[key] = 0
        self.data[key] += 1

    def append(self, key, value):
        if key not in self.data or not isinstance(self.data[key], list):
            self.data[key] = []
        self.data[key].append(value)

    def avg(self, key, value):
        if key not in self.data or not isinstance(self.data[key], Averager):
            self.data[key] = Averager()
        self.data[key].insert(value)

    def gauge(self, key, value):
        self.data[key] = value

    def rolling_avg(self, key, value, window):
        if key not in self.data or not isinstance(self.data[key], RollingAverager):
            self.data[key] = RollingAverager(window)
        self.data[key].insert(value)

    @contextlib.contextmanager
    def timer(self, key):
        start = time.time()
        try:
            yield
        finally:
            self.data[key] = time.time() - start

    @contextlib.contextmanager
    def avg_time(self, key):
        if key not in self.data or not isinstance(self.data[key], Averager):
            self.data[key] = Averager()
        start = time.time()
        try:
            yield
        finally:
            t = time.time() - start
            self.data[key].add_value(t)

    def __getitem__(self, key):
        return self.data[key]
