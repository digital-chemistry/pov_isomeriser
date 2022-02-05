# povs_isomeriser
This code can be used to generate all possible configurations of alfa-{V18O42} with beta-{V18O42} polyoxovanadates. The configurations are written out to files, sorted by the order of the average distance between the sites of substitution.   It can also be easily extended to solve for other geometries, as the underlying utilities are fairly generic. The code contains instructions on how to apply it to different situations. Feel free to contact me if you need any help with this.
The 2 runnable files are rbc_colorings.py and pseudo_rbc_colorings.py. You can run them from your IDE, or from your command line, for example:
python -m povs_isomeriser.rbc_colorings
(from the parent directory)

Code Author: Viktor Simjanoski 
The requirements are Python 3 and numpy, which can be installed by running pip install numpy
