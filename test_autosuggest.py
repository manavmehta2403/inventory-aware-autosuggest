import unittest
from autosuggest import Item, Search
class SearchTests(unittest.TestCase):
    def setUp(self):
        self.now=1000
        self.search=Search([Item('1','Paris Riverside Stay','Paris',True,990),Item('2','Paris Sold Out','Paris',False,990),Item('3','Paris Stale','Paris',True,500)],clock=lambda:self.now)
    def test_typo(self):
        self.assertEqual([i.id for i in self.search.suggest('pariss')],['1'])
    def test_normalization(self):
        self.assertEqual(self.search.suggest(' PÁRIS '),self.search.suggest('paris'))
    def test_expiry(self):
        self.search.suggest('paris'); self.now=1290
        self.assertEqual(self.search.suggest('paris'),[])
    def test_refresh(self):
        self.search.suggest('paris'); self.search.replace_inventory([])
        self.assertEqual(self.search.suggest('paris'),[])
    def test_capacity(self):
        self.search.capacity=2
        for q in ['paris','pariss','riverside']: self.search.suggest(q)
        self.assertEqual(len(self.search.cache),2)
    def test_short(self):
        self.assertEqual(self.search.suggest('p'),[])
    def test_limits(self):
        with self.assertRaises(ValueError): self.search.suggest('paris',0)
    def test_future(self):
        self.search.replace_inventory([Item('f','Paris','Paris',True,1100)])
        self.assertEqual(self.search.suggest('paris'),[])
if __name__=='__main__': unittest.main()
