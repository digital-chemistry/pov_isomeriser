'''
Created on Jul 3, 2017

@author: Viktor Simjanoski

Need Python 3 to run this, type in your terminal python rbc_colorings.py

Counting colorings for rhombicuboctahedron. We write them to a folder titled `out_rbc`, inside this local povs_isomeriser
directory. If the out directory already exists, the program will exit without writing anything. In this
case, you will need to rename or delete the existing `out` directory.
The run takes a few seconds.

If you want to generate colorings for a different configuration, you will need to copy this file to
a new file (let's call it new.py), and you will need to appropriately modify the functions below that
define the rotations (construct_rbc_rots()) and the distances (distance_between_two_vertices(v0, v1)).
Feel free to contact me on LinkedIn if you need any help.
'''
import datetime
import os
import sys
import numpy as np
from povs_isomeriser.rotation import Rotation
from povs_isomeriser.compose_rotations import all_rotations_combos
from povs_isomeriser.count_all_colorings import count_all_colorings
from povs_isomeriser.average_distance import average_distance
from povs_isomeriser.assert_rotations_and_distances import assert_rotations_and_distances

_VERTEX_LABELS = {'C2':1, 'B2':2, 'A2':3, 'B1':4, 'A1':5, 'C1':6,
                'b2c2':1, 'a2c2':2, 'b1c2':3, 'a1c2':4,
                'a2b2':5, 'a1b2':6, 'a1b1':7, 'a2b1':8,
                'a2c1':9, 'b2c1':10, 'a1c1':11, 'b1c1':12}
"""
4(3, 5) 781.5
2(5, 7) 754
2(8)4(5) 709.3
2(2, 7) 653
2(7, 9) 653
2(6, 7) 533.1
4(4, 5) 552
2(12)4(5) 543
2(7, 11) 377
2(7)4(5) 294

[('A1', '0'), ('A2', '0')]  #   4(3, 5)  # 781.5
[('A1', '0'), ('B1', '0')]  #   4(4, 5) # 552
[('A1', '0'), ('a1b1', '0')]  #  2(7) 4(5) # 294
[('A1', '0'), ('b1c1', '0')]  #  2(12) 4(5) # 543
[('A1', '0'), ('a2b1', '0')]  #  2(8) 4(5) # 709.3
[('a1b1', '0'), ('a1b2', '0')]  #  2(6,7)  # 533.1
[('a1b1', '0'), ('a1c1', '0')]  #  2(7,11) # 377
[('a1b1', '0'), ('a2b2', '0')]  #  2(5,7) # 754
[('a1b1', '0'), ('a2c1', '0')]  #  2(7,9) # 653
[('a1b1', '0'), ('a2c2', '0')]  #  2(2,7) # 653
"""

def _assert_vertices(v0, v1):
    assert not (v0 == v1)
    assert v0[0].lower() in ('a', 'b', 'c')
    assert v1[0].lower() in ('a', 'b', 'c')
    assert len(v0) in (2, 4)
    assert len(v1) in (2, 4)
    if len(v0) > 2:
        assert v0[2].lower() in ('a', 'b', 'c')
    if len(v1) > 2:
        assert v1[2].lower() in ('a', 'b', 'c')

def distance_between_two_vertices(v0, v1):
    """
    These are hard-coded distances based on experimental results.
    """
    _assert_vertices(v0, v1)
    
    if len(v0) == 2 and len(v1) == 2:  # both majors
        assert v0.upper() == v0
        assert v1.upper() == v1
        if v0[0] == v1[0]:
            return 781.5
        else:
            return 552
        
    if (len(v0) == 2 and len(v1) == 4) or (
        len(v0) == 4 and len(v1) == 2):
        v0, v1 = sorted([v0, v1], key=lambda x: len(x))
        assert len(v0) == 2 and len(v1) == 4
        if v0.lower() in (v1[:2], v1[2:]):  # adjacent major and minor
            return 294
        elif v0[0].lower() not in v1:
            return 543 
        elif v0[0].lower()  in v1:
            assert v0.lower() not in v1
            return 709.3
        
    if len(v0) == 4 and len(v1) == 4:
        assert v0.lower() == v0
        assert v1.lower() == v1
        if v0[0] == v1[0] and v0[2] == v1[2] and (v0[1] == v1[1] or v0[3] == v1[3]):
            return 533.1
        elif (v0[:2] == v1[:2]) or (v0[2:] == v1[:2]) or (
            (v0[:2] == v1[2:])) or (v0[2:] == v1[2:]) :
            assert not (v0[:3] == v1[:3])
            return 377
        elif v0[0] == v1[0] and v0[2] == v1[2]:
            assert not(v0[1] == v1[1] or v0[3] == v1[3]), '{} {}'.format(
                v0, v1)
            return 754
        elif (v0[0] == v1[0] and not (v0[2] == v1[2])) or (
            (v0[2] == v1[2] and not (v0[0] == v1[0]))) or (
             v0[0] == v1[2] and not (v0[2] == v1[0])) or (
             v0[2] == v1[0] and not (v0[0] == v1[0])):
            assert not (v0[:2] == v1[:2])
            assert not (v0[:2] == v1[2:])
            assert not (v0[2:] == v1[:2])
            assert not (v0[2:] == v1[2:])
            return 653 
        
        

def coloring_to_string(coloring):
    # better_labeled_coloring = {_VERTEX_LABELS[k]:v for k, v in coloring._iteritems()}
    zeros = [k for k, v in coloring if v in (0, '0')]
    twos = [vertex for vertex in zeros if len(vertex) == 4]
    fours = [vertex for vertex in zeros if len(vertex) == 2]
    assert len(twos) + len(fours) == len(zeros)
    
    twos = sorted([_VERTEX_LABELS[t] for t in twos])
    twos = [str(t) for t in twos]
    fours = sorted([_VERTEX_LABELS[f] for f in fours])
    fours = [str(f) for f in fours]
    twos_str = ','.join(twos)
    fours_str = ','.join(fours)
    twos_str = '2({}) '.format(twos_str) if len(twos_str) > 0 else ''
    fours_str = '4({})'.format(fours_str) if len(fours_str) > 0 else ''
    return twos_str + fours_str
    
def construct_rbc_rots():
    """
    Constructs all the relevant rotations.
    """
    rot1 = Rotation({
        'A1':'B1', 'B1':'A2', 'A2':'B2', 'B2':'A1', 'C1':'C1', 'C2':'C2',
        'a1b1':'a2b1', 'a2b1':'a2b2', 'a2b2':'a1b2', 'a1b2':'a1b1',
        'a1c1':'b1c1', 'b1c1':'a2c1', 'a2c1':'b2c1', 'b2c1':'a1c1',
         'a1c2':'b1c2', 'b1c2':'a2c2', 'a2c2':'b2c2', 'b2c2':'a1c2'})
    assert len(rot1.mapping) == 18
    assert rot1.degree == 4
    
    rot2 = Rotation({
        'A1':'C1', 'C1':'A2', 'A2':'C2', 'C2':'A1', 'B1':'B1', 'B2':'B2',
        'a1c1':'a2c1', 'a2c1':'a2c2', 'a2c2':'a1c2', 'a1c2':'a1c1',
        'a1b1':'b1c1', 'b1c1':'a2b1', 'a2b1':'b1c2', 'b1c2':'a1b1',
         'a1b2':'b2c1', 'b2c1':'a2b2', 'a2b2':'b2c2', 'b2c2':'a1b2'})
    assert len(rot2.mapping) == 18
    assert rot2.degree == 4
    
    rot3 = Rotation({
        'C1':'B1', 'B1':'C2', 'C2':'B2', 'B2':'C1', 'A1':'A1', 'A2':'A2',
        'b1c1':'b1c2', 'b1c2':'b2c2', 'b2c2':'b2c1', 'b2c1':'b1c1',
        'a1c1':'a1b1', 'a1b1':'a1c2', 'a1c2':'a1b2', 'a1b2':'a1c1',
         'a2c1':'a2b1', 'a2b1':'a2c2', 'a2c2':'a2b2', 'a2b2':'a2c1'})
    assert len(rot3.mapping) == 18
    assert rot3.degree == 4
    
    return all_rotations_combos([rot1, rot2, rot3])

def rbc_colorings():
    """
    Constructs all the different colorings.
    The colors are encoded as binary digits: 0s and 1s. We create the colorings by iterating
    over the number of zeros, which ranges from 2 to 9 (inclusive).
    """
    FOLDER_NAME = 'out_rbc'
    if os.path.isdir(FOLDER_NAME):
        print (f"The output directory {FOLDER_NAME} alredy exists, you can see it inside the alchemist folder.\nPlease rename it"+
                   " or delete it if you want to regenerate the output.\nOtherwise I am not doing anything. Exiting now.")
        return
    os.mkdir(FOLDER_NAME)
    all_rots = construct_rbc_rots()
    assert len(all_rots) == 24
    assert_rotations_and_distances(all_rots, distance_between_two_vertices)
    # number of zeros is number of vertices in a particular color, then ones is the number of the other color
    # you can think of it as blue color=zero red color=one
    for zeros in range(2, 10): 
        sys.stdout.flush()
        ones = 18 - zeros
        unique_colorings, _ = count_all_colorings(all_rots, zeros, ones)
        colorings_with_distances = []
        for coloring in unique_colorings:    
            zero_vertices = [p[0] for p in coloring if p[1] == '0']
            dist = average_distance(zero_vertices, distance_between_two_vertices)
            colorings_with_distances.append((coloring, dist))
        unique_colorings = [(coloring_to_string(cl), dist) for cl, dist in colorings_with_distances]
        unique_colorings = sorted(unique_colorings, key=lambda x: (-x[1], len(x[0]), x[0]))
  
        file_name = 'rbc_{}zeros_{}.txt'.format(zeros, len(unique_colorings))
        with open(f'{FOLDER_NAME}/{file_name}', 'w') as out_file:
                for ix, coloring in enumerate(unique_colorings, 1):
                    out_file.write('{}. {} {}\n'.format(ix, coloring[0], np.round(coloring[1], 2)))
                print (f'Writing {ix} colorings with {zeros} zeros to {file_name}')
        sys.stdout.flush()

    

    
if __name__ == '__main__':
    print ("Started at ", datetime.datetime.now())
    rbc_colorings()
    print ("Finished at ", datetime.datetime.now())
