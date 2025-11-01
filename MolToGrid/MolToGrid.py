import json
import numpy as np
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment
import ast
import matplotlib.pyplot as plt

## Read in the coordinates
with open('sample_data.json','r') as f:
    inputAtoms = json.load(f)

with open('albuquerque.json','r') as f:
    gridCoordsStrings = np.array(ast.literal_eval(f.read()))
    
inputCoords = []
for atom in inputAtoms:
    inputCoords.append([atom['x'],atom['y']])

print(type(inputCoords[0][0]))
print(type(gridCoords[0][0]))

def best_subset_assignment(A, B):
    """
    Find the subset of B that best matches A using the Hungarian algorithm.
    
    Parameters
    ----------
    A : (m, 2) array
        Small set of coordinates.
    B : (n, 2) array
        Large set of coordinates (n >= m).

    Returns
    -------
    subset : (m, 2) array
        Subset of B that best matches A.
    row_ind : array of ints
        Indices of A in the assignment.
    col_ind : array of ints
        Indices of B chosen for each A[i].
    mean_error : float
        Mean distance between matched points.
    """

    # Compute pairwise Euclidean distances
    D = distance_matrix(A, B)
    print("Made the matrix")

    # Run Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(D)
    print("Run algorithm")

    # Extract matched points
    subset = B[col_ind]
    print("Extracted subset")
    mean_error = D[row_ind, col_ind].mean()

    return subset, row_ind, col_ind, mean_error

print(best_subset_assignment(inputCoords,gridCoords)[0])

# Idea: Have some way to represent different elements differently?
# for atom1 in inputAtoms:
#    nodeNum=atom1['idx']
#    atom1Coords = [atom1['x'],atom1['y']]
#    for i in atom1['bonds']:
#         i=int(i)
#         if i>nodeNum:
#             atom2 = inputAtoms[i]
#             atom2Coords = [atom2['x'],atom2['y']]
#             plt.plot([atom1Coords[0],atom2Coords[0]],[atom1Coords[1],atom2Coords[1]],'ro-')

# plt.show()

# Need to put all coordinates in reference frame with sam's club
# Need to handle scaling somehow. 
# What measure can use to find best approximation of the molecule ignoring scale?