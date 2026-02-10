import unittest,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from cool_memories.core import FragmentEngine

class TestCool(unittest.TestCase):
    def test_theme(self):
        f=FragmentEngine()
        r=f.get_theme("america")
        self.assertIn("description",r)
    def test_fragment(self):
        f=FragmentEngine()
        r=f.generate_fragment("media")
        self.assertIsInstance(r,str)
    def test_analyze(self):
        f=FragmentEngine()
        r=f.analyze_fragment("America is the original version of modernity.")
        self.assertIn("word_count",r)
    def test_chronology(self):
        f=FragmentEngine()
        c=f.chronology()
        self.assertEqual(c[0]["year"],1929)

if __name__=="__main__": unittest.main()
