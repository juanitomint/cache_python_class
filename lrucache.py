# cache implementation server and client
from collections import defaultdict
from tabulate import tabulate
import hashlib
import json
import random
import logging

# Set the log level to DEBUG
logging.basicConfig(level=logging.DEBUG)


class Cache:
    def __init__(self, size, hash_key="id", tabulate=tabulate, logging=logging):
        self.cache_hits = defaultdict(int)
        self.cache_dict = {}
        self.size = size
        self.hash_key = hash_key
        self.tabulate = tabulate
        self.logger = logging.getLogger(__name__)

    # object ={key:value}
    def get(self, key):
        # hash=slelf.hash(object)
        # check first if hash exists on dict
        hash = self.hash({self.hash_key: key})
        if self.cache_dict.get(hash) != None:
            self.cache_hits[hash] += 1
            self.logger.debug(f"Cache hit {hash}")
            return self.cache_dict[hash]
        else:
            self.logger.debug(f"Cache miss for {hash}")
            return False

    def put(self, object):
        if len(self.cache_hits) >= self.size:
            self._evict()
        hash = self.hash(object)
        hits = 0
        if self.cache_dict.get(hash) != None:
            hits = self.cache_hits[hash]

        self.cache_dict[hash] = object
        self.cache_hits[hash] = hits
        self.logger.debug(f"Object with hash {hash} added to cache")

    def _evict(self):
        sorted_dict = dict(sorted(self.cache_hits.items(), key=lambda x: x[1]))
        last_key = list(sorted_dict.keys())[0]
        self.logger.debug(f"evicting key {last_key} from cache")

        self.invalidate(last_key)
        return True

    def invalidate(self, key):
        del self.cache_dict[key]
        del self.cache_hits[key]
        self.logger.debug(f"invalidating key {key} from cache")
        return True

    def hash(self, object):
        hash = hashlib.md5(object.get(self.hash_key).encode()).hexdigest()
        return hash

    def stats(self, cache_hits=True, cache_dict=False):
        if cache_hits:
            print(
                self.tabulate(
                    self.cache_hits.items(),
                    headers=["key", "Hits"],
                    tablefmt="simple_grid",
                )
            )
        if cache_dict:
            print(
                tabulate(
                    self.cache_dict.items(),
                    tablefmt="simple_grid",
                )
            )




cache = Cache(10, hash_key="id")
with open("data.json", "r") as f:
    data = json.load(f)


print("populate 10 first objects")
for entry in data[:10]:  # Iterate through the first ten entries in the data
    cache.put(entry)
cache.stats(tabulate)
print("Emulate some random 'gets' hits and misses")
for i in range(0, 100):
    random_number = random.randint(0, 14)
    cache.get(data[random_number].get("id"))
cache.stats(tabulate)

print("insert new key and evict less used")
entry = data[10]
cache.put(entry)
cache.stats(tabulate)
