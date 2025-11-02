import json
from pathlib import Path

import numpy as np
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment, minimize_scalar

R = Path(__file__).parent.parent


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
        ## Simply the matrix of distances between all the points in A and all the points in B
        D = distance_matrix(A_centered, B_scaled)
        row_ind, col_ind = linear_sum_assignment(D)
        return D[row_ind, col_ind].mean()

    print("Optimising for scale")
    if optimize_scale:
        # Optimize the scale factor to minimize mean matching error
        res = minimize_scalar(mean_error_for_scale, bounds=(0.001, 700), method='bounded')
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
    print(f"Error: {mean_error}")

    return subset, mean_error


def MolToGrid(atom_json, is_cam=False):
    # How much error we're willing to accept between the road intersections and the molecule
    acceptableError = 0.05

    inputAtoms = atom_json

    ## How far outside of central alberquerque we're willing to go
    tolerance = 0

    while True:
        print(f"Tolerance: {tolerance}")
        print("reading")
        p = f"MolToGrid/filtereds/albNPFiltered{tolerance}.txt" if not is_cam \
            else "MolToGrid/cambNP.txt"
        gridCoords = np.loadtxt(R / p, dtype=float)
        print("done reading")

        inputCoords = []
        for atom in inputAtoms:
            inputCoords.append([atom['x'], atom['y']])
        inputCoords = np.array(inputCoords)
        albPoints, error = best_subset_assignment(inputCoords, gridCoords)
        tolerance += 0.1
        if error < acceptableError:
            break

    pairs = set()
    ll_to_at = {}
    for i, (lat, lng) in enumerate(albPoints.tolist()):
        atom_json[i]['alb'] = lat, lng
        ll_to_at[(lat, lng)] = atom_json[i]["element"]
    for a in atom_json:
        for idx_s in a["bonds"]:
            bi = int(idx_s)
            b = atom_json[bi]
            pairs.add(frozenset((a['alb'], b['alb'])))
    return pairs, ll_to_at


if __name__ == '__main__':
    with open('../MolToGrid/sample_data.json') as f:
        j = json.load(f)
    print(MolToGrid(j))
