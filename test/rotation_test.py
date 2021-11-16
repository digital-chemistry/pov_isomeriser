'''
Created on Jul 2, 2017

@author: Viktor Simjanoski
'''
import unittest
from povs_isomeriser.rotation import Rotation


class RotationTest(unittest.TestCase):
    def test1_cycle2(self):
        rot1 = Rotation(mapping={1:1, 2:2})
        self.assertEqual(rot1.degree, 1)
        rot2 = Rotation(mapping={2:2, 1:1})
        self.assertEqual(rot1, rot2)
        all_rots = set([rot1, rot2])
        self.assertEqual(len(all_rots), 1)

    def test2_cycle2(self):
        rot1 = Rotation(mapping={1:2, 2:1})
        self.assertEqual(rot1.degree, 2)
        rot2 = Rotation(mapping={2:1, 1:2})
        self.assertEqual(rot1, rot2)
        all_rots = set([rot1, rot2])
        self.assertEqual(len(all_rots), 1)
        
    def test1_cycle3(self):
        rot1 = Rotation(mapping={1:2, 2:3, 3:1})
        self.assertEqual(rot1.degree, 3)
        rot2 = Rotation(mapping={ 2:3, 1:2, 3:1})
        rot3 = Rotation(mapping={ 2:3, 3:1, 1:2})
        self.assertEqual(rot1, rot2)
        self.assertEqual(rot2, rot3)
        all_rots = set([rot1, rot2, rot3])
        self.assertEqual(len(all_rots), 1)
        
    def test2_cycle3(self):
        rot = Rotation(mapping={1:3, 2:1, 3:2})
        self.assertEqual(rot.degree, 3)
        
    def test1_cycle4(self):
        rot = Rotation(mapping={1:2, 2:3, 3:4, 4:1})
        self.assertEqual(rot.degree, 4)
        rot2 = rot.power(2)
        self.assertEqual(rot2, Rotation({1:3, 2:4, 3:1, 4:2}))
    
    def test2_cycle4(self):
        rot = Rotation(mapping={1:3, 2:4, 3:1, 4:2})
        self.assertEqual(rot.degree, 2)
        rot2 = rot.power(4)
        self.assertEqual(rot2, Rotation({1:1, 2:2, 3:3, 4:4}))
        
        
    def test3_cycle4(self):
        rot = Rotation(mapping={1:4, 2:1, 3:2, 4:3})
        self.assertEqual(rot.degree, 4)
        rot2 = rot.power(2)
        self.assertEqual(rot2, Rotation({1:3, 2:4, 3:1, 4:2}))
        rot8 = rot.power(8)
        self.assertEqual(rot8, Rotation({1:1, 2:2, 3:3, 4:4}))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
