'''
Created on Jul 8, 2017

@author: Viktor Simjanoski

Counting colorings for pseudo-rhombicuboctahedron. The file structure is same as rbc_colorings.py
(please check the documentation there). Only difference is the hard-coded structure of the solid
and the distances between various vertices.
The run takes 1-2 minutes depending on your computer.
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


_VERTEX_LABELS = {'X1':1, 'X2':2,
                  'd2x1':1, 'b1x1':2, 'd1x1':3, 'b2x1':4,
                  'a1x2':5, 'c1x2':6, 'a2x2':7, 'c2x2':8,
                  'A1':1, 'B1':2, 'C1':3, 'D1':4, 'A2':5, 'B2':6, 'C2':7, 'D2':8}


def _assert_vertices(v0, v1):
    assert not (v0 == v1)
    assert v0[0].lower() in ('a', 'b', 'c', 'd', 'x', 'y')
    assert v1[0].lower() in ('a', 'b', 'c', 'd', 'x', 'y')
    assert len(v0) in (2, 4)
    assert len(v1) in (2, 4)
    if len(v0) > 2:
        assert v0[2].lower() in ('x', 'y')
    if len(v1) > 2:
        assert v1[2].lower() in ('x', 'y')
        
def _distance_between_vertices_of_length_2(v0, v1):
    if v0 == 'X1' and v1 == 'X2':  # opposite poles
            return 8.1092
    else: 
        # pole - equator
        assert not (v0[0] == 'X' and v1[0]=='X')
        if (v0, v1) in [('B1', 'X2'), ('D1', 'X2'), ('A1', 'X1'), ('C1', 'X1'), ('A2', 'X1'),
                       ('C2', 'X1'), ('B2', 'X2'), ('D2', 'X2')]:
            return 5.5633
        elif (v0, v1) in [('D2', 'X1'), ('B2', 'X1'), ('B1', 'X1'), ('D1', 'X1'),
                         ('C1', 'X2'), ('A2', 'X2'), ('A1', 'X2'), ('C2', 'X2')]:
            return 5.7835
        
        # equator
        # neighbors on the equator
        if (v0, v1) in [('A1', 'B1'), ('B1', 'C1'), ('C1', 'D1'), ('A2', 'D1'),
                    ('A2', 'B2'), ('B2', 'C2'), ('C2', 'D2'), ('A1', 'D2')]:  
            return 3.0517
        # dist=2 on the equator
        if (v0, v1) in [('A1', 'C1'), ('B1', 'D1'), ('A2', 'C1'), ('B2', 'D1'),
                        ('A2', 'C2'), ('B2', 'D2'), ('A1', 'C2'), ('B1', 'D2')]:
            return 5.61
        # dist=3 on the equator
        if (v0, v1) in [('A1', 'D1'), ('A2', 'B1'), ('B2', 'C1'), ('C2', 'D1'),
                        ('A2', 'D2'), ('A1', 'B2'), ('B1', 'C2'), ('C1', 'D2')]:
            return 7.3363
        # dist=4(opposites) on the equator
        if (v0, v1) in [('A1', 'A2'), ('B1', 'B2'), ('C1', 'C2'), ('D1', 'D2')]:
            return 7.9338
    raise Exception('Unknows distance between {} and {}'.format(v0, v1))
        
def _distance_between_vertices_of_length_4(v0, v1):
    if v0[2:] == v1[2:]:  # same hemisphere
        # neighbors, same hemisphere
        if (v0[:2], v1[:2]) in [('b1', 'd2'), ('b1', 'd1'), ('b2', 'd1'), ('b2', 'd2'),
                                ('a1', 'c1'), ('a2', 'c1'), ('a2', 'c2'), ('a1', 'c2')]:
            return 3.8575
        # opposites, same hemisphere
        if (v0[:2], v1[:2]) in [('a1', 'a2'), ('b1', 'b2'), ('c1', 'c2'), ('d1', 'd2')]:
            return 5.4554
        
    elif (v0[2:], v1[2:]) in[('x1', 'x2'), ('x2', 'x1')]:
        if (v0[:2], v1[:2]) in [('a1', 'b1'), ('b1', 'c1'), ('c1', 'd1'), ('a2', 'd1'),
                                ('a2', 'b2'), ('b2', 'c2'), ('c2', 'd2'), ('a1', 'd2')]:
            
            return 5.7815
        if (v0[:2], v1[:2]) in [('a1', 'd1'), ('a2', 'b1'), ('b2', 'c1'), ('c2', 'd1'),
                                ('a2', 'd2'), ('a1', 'b2'), ('b1', 'c2'), ('c1', 'd2')]:
            return 7.3804
    raise Exception('Unknows distance between {} and {}'.format(v0, v1))

def _distance_between_vertices_of_length_2_4(v0, v1):
    # neighbors, one is pole
    if (v0, v1) in [('X1', 'd1x1'), ('X1', 'b1x1'), ('X1', 'd2x1'), ('X1', 'b2x1'),
                  ('X2', 'c1x2'), ('X2', 'a2x2'), ('X2', 'a1x2'), ('X2', 'c2x2')]:
        assert v0.lower()  in v1
        return 3.0474
    # opposites
    elif (v0, v1) in [('X1', 'c1x2'), ('X1', 'a2x2'), ('X1', 'a1x2'), ('X1', 'c2x2'),
                  ('X2', 'd1x1'), ('X2', 'b1x1'), ('X2', 'd2x1'), ('X2', 'b2x1')]:
        assert v0.lower() not in v1
        return 7.2806
    else:  # middle_arc - equator
        assert not v0.startswith('X'), '{} {}'.format(v0, v1)  # neighbors
        if v1.startswith(v0.lower()):
            return 3.1076
        elif v0[0].lower() == v1[0].lower():  # opposites
            assert not (v0.lower() in v1[0].lower())
            return 7.2759
        elif tuple(sorted([v0.lower(), v1[:2].lower()])) in [('a1', 'b1'), ('b1', 'c1'), ('c1', 'd1'), ('a2', 'd1'),
                                              ('a2', 'b2'), ('b2', 'c2'), ('c2', 'd2'), ('a1', 'd2')]:
            return 3.786
        

        elif (v0.lower(), v1[:2].lower()) in [('a1', 'c1'), ('c1', 'a1'), ('a1', 'c2'), ('c2', 'a1'),
                                              ('a2', 'c1'), ('c1', 'a2'), ('a2', 'c2'), ('c2', 'a2'),
                                              ('b1', 'd1'), ('d1', 'b1'), ('b1', 'd2'), ('d2', 'b1'),
                                              ('b2', 'd1'), ('d1', 'b2'), ('b2', 'd2'), ('d2', 'b2')]:
            return 5.5944
        
        
        elif (v0.lower(), v1[:2].lower()) in [('a1', 'd1'), ('d1', 'a1'), ('a1', 'b2'), ('b2', 'a1'),
                                              ('b1', 'a2'), ('a2', 'b1'), ('b1', 'c2'), ('c2', 'b1'),
                                              ('b2', 'c1'), ('c1', 'b2'), ('d1', 'c2'), ('c2', 'd1'),
                                              ('a2', 'd2'), ('d2', 'a2'), ('c1', 'd2'), ('d2', 'c1')]:
            return 6.7036
        

    raise Exception('Unknows distance between {} and {}'.format(v0, v1))

def distance_between_two_vertices(v0, v1):
    _assert_vertices(v0, v1)
    v0, v1 = sorted([v0, v1], key=lambda x: (len(x), x))
    if len(v0) == 2 and len(v1) == 2:
        return _distance_between_vertices_of_length_2(v0, v1)

            
    if len(v0) == 2 and len(v1) == 4:
        return _distance_between_vertices_of_length_2_4(v0, v1)
                
        
    if len(v0) == 4 and len(v1) == 4:
        return _distance_between_vertices_of_length_4(v0, v1)
        
    raise Exception('Unknows distance between {} and {}'.format(v0, v1))
    
        

def coloring_to_string(coloring):
    """
    better_labeled_coloring = {_VERTEX_LABELS[k]:v for k, v in coloring._iteritems()}
    """
    zeros = [k for k, v in coloring if v in (0, '0')]
    twos = [vertex for vertex in zeros if len(vertex) == 4]
    threes = [vertex for vertex in zeros if len(vertex) == 2 and (
        vertex.startswith('A') or vertex.startswith('B') or vertex.startswith('C')
        or vertex.startswith('D'))]
    fours = [vertex for vertex in zeros if vertex in ('X1', 'X2')]
    assert len(twos) + len(threes) + len(fours) == len(zeros)
    
    twos = sorted([_VERTEX_LABELS[t] for t in twos])
    twos = [str(t) for t in twos]
    
    threes = sorted([_VERTEX_LABELS[f] for f in threes])
    threes = [str(f) for f in threes]
    
    fours = sorted([_VERTEX_LABELS[f] for f in fours])
    fours = [str(f) for f in fours]
    
    
    twos_str = ','.join(twos)
    threes_str = ','.join(threes)
    fours_str = ','.join(fours)
    
    twos_str = '2({}) '.format(twos_str) if len(twos_str) > 0 else ''
    threes_str = '3({}) '.format(threes_str) if len(threes_str) > 0 else ''
    fours_str = '4({})'.format(fours_str) if len(fours_str) > 0 else ''
    return twos_str + threes_str + fours_str
    
def construct_pseudo_rbc_rots():
    rot1 = Rotation({'X1':'X1', 'X2':'X2', 'A1':'C1', 'B1':'D1', 'C1':'A2',
                     'D1':'B2', 'A2':'C2', 'B2':'D2', 'C2':'A1', 'D2':'B1',
                     'a1x2':'c1x2', 'c1x2':'a2x2', 'a2x2':'c2x2', 'c2x2':'a1x2',
                     'b1x1':'d1x1', 'd1x1':'b2x1', 'b2x1':'d2x1', 'd2x1':'b1x1'})
    assert len(rot1.mapping) == 18
    assert rot1.degree == 4
    
    rot2 = Rotation({'X1':'X2', 'X2':'X1', 'A1':'B1', 'B1':'A1', 'A2':'B2',
                     'B2':'A2', 'C1':'D2', 'D2':'C1', 'C2':'D1', 'D1':'C2',
                     'a1x2':'b1x1', 'c1x2':'d2x1', 'a2x2':'b2x1', 'c2x2':'d1x1',
                     'b1x1':'a1x2', 'd1x1':'c2x2', 'b2x1':'a2x2', 'd2x1':'c1x2'})
    assert len(rot2.mapping) == 18
    assert rot2.degree == 2
    
    return all_rotations_combos([rot1, rot2])


            
def pseudo_rbc_colorings():
    FOLDER_NAME = 'out_prbc'
    if os.path.isdir(FOLDER_NAME):
        print (f"The output directory {FOLDER_NAME} alredy exists, you can see it inside this folder.\nPlease rename it"+
                   " or delete it if you want to regenerate the output.\nOtherwise I am not doing anything. Exiting now.")
        return
    os.mkdir(FOLDER_NAME)
    
    all_rots = construct_pseudo_rbc_rots()
    assert len(all_rots) == 8, len(all_rots)
    assert_rotations_and_distances(all_rots, distance_between_two_vertices)
    # number of zeros is number of vertices in a particular color, then ones is the number of the other color
    # you can think of it as blue color=zero red color=one
    for zeros in range(1, 10):
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
  
        file_name = 'pseudo_rbc_{}zeros_{}.txt'.format(zeros, len(unique_colorings))
        with open(f'{FOLDER_NAME}/{file_name}', 'w') as out_file:
            for ix, coloring in enumerate(unique_colorings, 1):
                out_file.write('{}. {} {}\n'.format(ix, coloring[0], np.round(coloring[1], 8)))
            print (f'Writing {ix} colorings with {zeros} zeros to {file_name}')
        sys.stdout.flush()

    

    
if __name__ == '__main__':
    print ("Started at ", datetime.datetime.now())
    pseudo_rbc_colorings()
    print ("Finished at ", datetime.datetime.now())
