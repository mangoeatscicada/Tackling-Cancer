import unittest
from watson import watson

class TestWatson(unittest.TestCase):

    def test_blood(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_cancer(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_other(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_zip(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_main(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWatson)
    unittest.TextTestRunner(verbosity=2).run(suite)