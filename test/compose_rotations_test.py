'''
Created on Jul 3, 2017

@author: Viktor Simjanoski
'''
import unittest
from povs_isomeriser.rotation import Rotation
from povs_isomeriser.compose_rotations import compose_rotations, \
    all_rotations_combos


class ComposeRotationsTest(unittest.TestCase):


    def test_compose1(self):
        rot1 = Rotation(mapping={1:2, 2:1})
        rot2 = compose_rotations([rot1, rot1])
        self.assertEqual(rot2, Rotation({1:1, 2:2}))
        
    def test_compose2(self):
        rot1 = Rotation(mapping={1:3, 2:4, 3:1, 4:2})
        rot2 = Rotation(mapping={1:2, 2:3, 3:4, 4:1})
        rot3 = compose_rotations([rot1, rot2])
        self.assertEqual(rot3, Rotation({1:4, 2:1, 3:2, 4:3}))
        
    def test_compose3(self):
        rot1 = Rotation(mapping={1:3, 2:4, 3:1, 4:2})
        rot2 = Rotation(mapping={1:2, 2:3, 3:4, 4:1})
        rot3 = Rotation(mapping={2:1, 3:2, 4:3, 1:4})
        rot4 = compose_rotations([rot1, rot2, rot3])
        self.assertEqual(rot4, Rotation({1:3, 2:4, 3:1, 4:2}))
        rot5 = compose_rotations([rot1, rot3, rot2])
        rot6 = compose_rotations([rot2, rot3, rot1])
        rot7 = compose_rotations([rot2, rot1, rot3])
        self.assertEqual(rot5, rot6)
        self.assertEqual(rot5, rot7)
        self.assertEqual(rot4, rot7)
        all_rots = set([rot1, rot2, rot3, rot4, rot5, rot6, rot7])
        self.assertEqual(len(all_rots), 3)
        
    def test_all_combos1(self):
        rot1 = Rotation(mapping={1:2, 2:1})
        all_rots = all_rotations_combos([rot1])
        self.assertEqual(len(all_rots), 2)
        
    def test_all_combos2(self):
        rot1 = Rotation(mapping={1:3, 2:4, 3:1, 4:2})
        all_rots = all_rotations_combos([rot1])
        self.assertEqual(len(all_rots), 2)
        
    def test_all_combos3(self):
        rot1 = Rotation(mapping={'A1':'B1', 'B1':'A2', 'A2':'B2', 'B2':'A1', 'C1':'C1', 'C2':'C2'})
        rot2 = Rotation(mapping={'A1':'C1', 'C1':'A2', 'A2':'C2', 'C2':'A1', 'B1':'B1', 'B2':'B2'})
        rot3 = Rotation(mapping={'B1':'C1', 'C1':'B2', 'B2':'C2', 'C2':'B1', 'A1':'A1', 'A2':'A2'})
        all_rots = all_rotations_combos([rot1, rot2, rot3])
        self.assertEqual(len(all_rots), 24)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
