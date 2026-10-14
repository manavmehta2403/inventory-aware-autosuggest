"""Independent example. Synthetic inventory only."""
from collections import OrderedDict
from dataclasses import dataclass
from time import time
from unicodedata import normalize
from rapidfuzz.fuzz import WRatio

def normalized(text):
    return ' '.join(normalize('NFKD', text).encode('ascii', 'ignore').decode().lower().split())

@dataclass(frozen=True)
class Item:
    id: str
    name: str
    city: str
    available: bool
    observed_at: float

class Search:
    def __init__(self, items, freshness=300, cache_size=128, clock=time):
        if freshness <= 0 or cache_size < 1:
            raise ValueError('Freshness and capacity must be positive')
        self.items = tuple(items)
        self.freshness = freshness
        self.capacity = cache_size
        self.clock = clock
        self.cache = OrderedDict()

    def replace_inventory(self, items):
        self.items = tuple(items)
        self.cache.clear()

    def suggest(self, query, limit=5):
        if not 1 <= limit <= 20:
            raise ValueError('Limit must be 1 to 20')
        query = normalized(query)
        if len(query) < 2:
            return []
        now = self.clock()
        cached = self.cache.get((query, limit))
        if cached and now < cached[0]:
            self.cache.move_to_end((query, limit))
            return list(cached[1])
        eligible = [i for i in self.items if i.available and 0 <= now-i.observed_at < self.freshness]
        ranked = []
        for item in eligible:
            target = normalized(item.name+' '+item.city)
            score = 100 if target.startswith(query) else WRatio(query, target)
            if score >= 70:
                ranked.append((score, item))
        ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
        result = tuple(i for _, i in ranked[:limit])
        expires = min([now+30]+[i.observed_at+self.freshness for i in eligible])
        self.cache[(query, limit)] = (expires, result)
        self.cache.move_to_end((query, limit))
        while len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
        return list(result)

if __name__ == '__main__':
    now = time()
    search = Search([Item('demo-1', 'Paris Riverside Stay', 'Paris', True, now),
                     Item('demo-2', 'Paris Garden Stay', 'Paris', False, now)])
    print([i.name for i in search.suggest('pariss')])
