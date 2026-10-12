"""Tiny numpy-only distance transform (avoids a scipy dependency)."""
import numpy as np


def dist_transform(grid):
    """Distance from each cell to the nearest occupied (==1) cell."""
    occ = np.argwhere(grid == 1)
    n, m = grid.shape
    out = np.zeros(grid.shape)
    for i in range(n):
        for j in range(m):
            out[i, j] = np.sqrt(((occ - [i, j]) ** 2).sum(1)).min()
    return out
