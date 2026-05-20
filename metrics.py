import numpy as np

def edge_density(edge_image, threshold=50):

    binary_edges = edge_image > threshold

    density = np.count_nonzero(binary_edges) / binary_edges.size

    return round(density * 100, 2)