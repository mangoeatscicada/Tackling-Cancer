import unittest
import tackling_cancer.models.watson as watson
import tackling_cancer.views.views as views

class TestWatson(unittest.TestCase):

    def test_blood(self):
        self.assertEqual(views.jsonType(watson.classify(['tests/blood_img_test.jpg'])), 'blood')

    def test_cancer(self):
        self.assertEqual(views.jsonType(watson.classify(['tests/cancer_img_test.jpg'])), 'cancer')

    def test_other(self):
        self.assertEqual(views.jsonType(watson.classify(['tests/other_img_test.jpg'])), 'other')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWatson)
    unittest.TextTestRunner(verbosity=2).run(suite)