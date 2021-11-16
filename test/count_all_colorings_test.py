'''
Created on Jul 3, 2017

@author: Viktor Simjanoski
'''
import unittest
from povs_isomeriser.compose_rotations import all_rotations_combos
from povs_isomeriser.rotation import Rotation
from povs_isomeriser.count_all_colorings import count_all_colorings


class CountAllColoringsTest(unittest.TestCase):


    def test_square1(self):
        all_rotations = all_rotations_combos([Rotation({1:2, 2:3, 3:4, 4:1})])
        unique_colorings, _ = count_all_colorings(all_rotations, zeros=1, ones=3)
        self.assertEqual(len(unique_colorings), 1)
        
    def test_square2(self):
        all_rotations = all_rotations_combos([Rotation({1:4, 2:1, 3:2, 4:3})])
        unique_colorings, _ = count_all_colorings(all_rotations, zeros=2, ones=2)
        self.assertEqual(len(unique_colorings), 2)
        
    def test_cube(self):
        rot1 = Rotation(mapping={'A1':'B1', 'B1':'A2', 'A2':'B2', 'B2':'A1', 'C1':'C1', 'C2':'C2'})
        rot2 = Rotation(mapping={'A1':'C1', 'C1':'A2', 'A2':'C2', 'C2':'A1', 'B1':'B1', 'B2':'B2'})
        rot3 = Rotation(mapping={'B1':'C1', 'C1':'B2', 'B2':'C2', 'C2':'B1', 'A1':'A1', 'A2':'A2'})
        all_rots = all_rotations_combos([rot1, rot2, rot3])
        all_ways = 0
        for zeros in range(0, 7):
            ones = 6 - zeros
            unique_colorings, _ = count_all_colorings(all_rots, zeros=zeros, ones=ones)
            all_ways +=len(unique_colorings)
        self.assertEqual(all_ways, 10)
            


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
