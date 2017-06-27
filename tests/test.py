import unittest
from watson import watson_test
from tackling_cancer import tackling_cancer

class TestWatson(unittest.TestCase):

    def test_blood(self):
        self.assertEqual(tackling_cancer.jsonType(watson_test.classify(['tests/blood_img_test.jpg'])), 'blood')

    def test_cancer(self):
        self.assertEqual(tackling_cancer.jsonType(watson_test.classify(['tests/cancer_img_test.jpg'])), 'cancer')

    def test_other(self):
        self.assertEqual(tackling_cancer.jsonType(watson_test.classify(['tests/other_img_test.jpg'])), 'other')

    def test_zip(self):
        self.assertEqual(tackling_cancer.jsonType(watson_test.classify(['tests/zip_test.zip'])), 'blood')

    def test_main(self):
        self.assertEqual(tackling_cancer.jsonType(watson_test.classify(['tests/blood_img_test.jpg'])), 'blood')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWatson)
    unittest.TextTestRunner(verbosity=2).run(suite)