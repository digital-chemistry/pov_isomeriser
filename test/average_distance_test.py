'''
Created on Jul 7, 2017

@author: Viktor Simjanoski
'''
import unittest
from povs_isomeriser.average_distance import average_distance

class AverageDistanceTest(unittest.TestCase):


    def test1(self):
        points = [1, 2, 3]
        distance_func = lambda x, y:  abs(x - y)
        self.assertAlmostEqual(average_distance(points, distance_func), 4.0 / 3, places=7)
        
    def test2(self):
        points = [1, 2, 3, 4]
        distance_func = lambda x, y:  abs(x - y)
        self.assertAlmostEqual(average_distance(points, distance_func), 5.0 / 3, places=7)


if __name__ == "__main__":
    unittest.main()
