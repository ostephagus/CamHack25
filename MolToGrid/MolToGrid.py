import json
import numpy as np
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment, minimize_scalar
import ast
import matplotlib.pyplot as plt

## Read in the coordinates
with open('sample_data.json','r') as f:
    inputAtoms = json.load(f)

print("reading")
gridCoords = np.loadtxt("albNP.txt",dtype=float)
print("done reading")

# with open('albuquerque.json','r') as f:
#     print("reading")
#     gridCoords = np.array(ast.literal_eval(f.read()))
#     print("done reading")

inputCoords = []
for atom in inputAtoms:
    inputCoords.append([atom['x'],atom['y']])

inputCoords = np.array(inputCoords)

# def best_subset_assignment(A, B):
#     print("started")
#     """
#     Find the subset of B that best matches A using the Hungarian algorithm.
    
#     Parameters
#     ----------
#     A : (m, 2) array
#         Small set of coordinates.
#     B : (n, 2) array
#         Large set of coordinates (n >= m).

#     Returns
#     -------
#     subset : (m, 2) array
#         Subset of B that best matches A.
#     row_ind : array of ints
#         Indices of A in the assignment.
#     col_ind : array of ints
#         Indices of B chosen for each A[i].
#     mean_error : float
#         Mean distance between matched points.
#     """

#     # Compute pairwise Euclidean distances
#     D = distance_matrix(A, B)
#     print("Made the matrix")

#     # Run Hungarian algorithm
#     row_ind, col_ind = linear_sum_assignment(D)
#     print("Run algorithm")

#     # Extract matched points
#     subset = B[col_ind]
#     print("Extracted subset")
#     mean_error = D[row_ind, col_ind].mean()

#     return subset, row_ind, col_ind, mean_error

# def best_subset_assignment(A, B, center=True):
#     """
#     Find the subset of B that best matches A using the Hungarian algorithm,
#     optionally accounting for translation (centering).

#     Parameters
#     ----------
#     A : (m, 2) array
#         Small set of coordinates.
#     B : (n, 2) array
#         Large set of coordinates (n >= m).
#     center : bool, optional
#         If True, both sets are centered before matching (translation-invariant).

#     Returns
#     -------
#     subset : (m, 2) array
#         Subset of B (in original coordinates) that best matches A.
#     row_ind : array of ints
#         Indices of A in the assignment.
#     col_ind : array of ints
#         Indices of B chosen for each A[i].
#     mean_error : float
#         Mean distance between matched points after centering.
#     translation : (2,) array
#         Translation vector applied to B to align centroids with A.
#     """

#     if center:
#         # Compute centroids
#         A_centroid = A.mean(axis=0)
#         B_centroid = B.mean(axis=0)

#         # Center both sets
#         A_centered = A - A_centroid
#         B_centered = B - B_centroid

#         # Compute pairwise distances
#         D = distance_matrix(A_centered, B_centered)
#         translation = B_centroid - A_centroid
#     else:
#         D = distance_matrix(A, B)
#         translation = np.zeros(2)

#     # Run Hungarian algorithm
#     row_ind, col_ind = linear_sum_assignment(D)

#     # Extract matched points (in original coordinates)
#     subset = B[col_ind]

#     # Compute mean error
#     mean_error = D[row_ind, col_ind].mean()

#     return subset, row_ind, col_ind, mean_error, translation

def best_subset_assignment(A, B, optimize_scale=True):
    """
    Find the subset of B that best matches A using the Hungarian algorithm,
    accounting for translation and (optionally) scaling.

    Parameters
    ----------
    A : (m, 2) array
        Small set of coordinates.
    B : (n, 2) array
        Large set of coordinates (n >= m).
    optimize_scale : bool, optional
        If True, optimizes a scale factor to minimize mean matching error.

    Returns
    -------
    subset : (m, 2) array
        Subset of B (in original coordinates) that best matches A.
    row_ind : array of ints
        Indices of A in the assignment.
    col_ind : array of ints
        Indices of B chosen for each A[i].
    mean_error : float
        Mean distance between matched points after transformation.
    translation : (2,) array
        Translation vector applied to align B’s centroid with A’s centroid.
    scale : float
        Optimal scaling factor applied to B.
    """

    # Compute centroids
    A_centroid = A.mean(axis=0)
    B_centroid = B.mean(axis=0)

    # Center both sets
    A_centered = A - A_centroid
    B_centered = B - B_centroid

    print("Computing error for scale")
    def mean_error_for_scale(s):
        """Compute mean assignment error for a given scale s."""
        B_scaled = B_centered * s
        D = distance_matrix(A_centered, B_scaled)
        row_ind, col_ind = linear_sum_assignment(D)
        return D[row_ind, col_ind].mean()

    print("Optimising for scale")
    if optimize_scale:
        # Optimize the scale factor to minimize mean matching error
        res = minimize_scalar(mean_error_for_scale, bounds=(0.1, 10), method='bounded')
        best_scale = res.x
    else:
        best_scale = 1.0
    print("Done optimising")

    # Final matching using optimal scale
    B_scaled = B_centered * best_scale
    D = distance_matrix(A_centered, B_scaled)
    row_ind, col_ind = linear_sum_assignment(D)
    mean_error = D[row_ind, col_ind].mean()

    # Compute translation (to bring scaled B back to A’s position)
    translation = A_centroid - (B_centroid * best_scale)

    # Subset in original coordinate space
    subset = B[col_ind]

    return subset, row_ind, col_ind, mean_error, translation, best_scale

# The points in albuquerque that represent the molecule
albPoints = best_subset_assignment(inputCoords,gridCoords)[0]

with open("albCoordsOfMolecule.txt","w+") as f:
    for i in albPoints:
        f.write(str(float(i[0]))+" "+str(float(i[1]))+"\n")

## Adjacency list for the bonds
bondData = [[{int(j):i['bonds'][j]['order']} for j in i['bonds']] for i in inputAtoms]

with open("albBondData.txt", "w+") as f:
    f.write(str(bondData))

#Idea: Have some way to represent different elements differently?
for i in range(len(albPoints)):
   coords1 = albPoints[i]
   atom1 =inputAtoms[i]
   nodeNum=atom1['idx']
   for j in atom1['bonds']:
        j=int(j)
        if j>nodeNum:
            atom2 = inputAtoms[j]
            coords2 = albPoints[j]
            plt.plot([coords1[0],coords2[0]],[coords1[1],coords2[1]],'ro-')
# for atom1 in inputAtoms:
#    nodeNum=atom1['idx']
#    atom1Coords = [atom1['x'],atom1['y']]
#    for i in atom1['bonds']:
#         i=int(i)
#         if i>nodeNum:
#             atom2 = inputAtoms[i]
#             atom2Coords = [atom2['x'],atom2['y']]
#             plt.plot([atom1Coords[0],atom2Coords[0]],[atom1Coords[1],atom2Coords[1]],'ro-')

plt.show()

# Need to put all coordinates in reference frame with sam's club
# Need to handle scaling somehow. 
# What measure can use to find best approximation of the molecule ignoring scale?