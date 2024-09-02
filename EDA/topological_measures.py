import numpy as np
import networkx as nx
from bct import clustering_coef_bu
from bct import distance_bin
from bct import efficiency_bin

def calculate_clustering_coefficients(connectivity_matrix, random_matrices):
    # Local Clustering Coefficient
    G = nx.from_numpy_array(connectivity_matrix)
    local_clustering = clustering_coef_bu(connectivity_matrix)
    absolute_clustering_coefficient = np.mean(local_clustering)
    # Normalized Clustering Coefficient
    random_clustering_coeffs = []
    for random_matrix in random_matrices:
        random_clustering = clustering_coef_bu(random_matrix)
        random_clustering_coeffs.append(np.mean(random_clustering))
    Crandom = np.mean(random_clustering_coeffs)
    normalized_clustering_coefficient = absolute_clustering_coefficient / Crandom
    
    return absolute_clustering_coefficient, normalized_clustering_coefficient

def calculate_characteristic_path_length(connectivity_matrix, random_matrices):
    D = distance_bin(connectivity_matrix)
    L = np.mean(D[np.isfinite(D)])
    random_path_lengths = []
    for random_matrix in random_matrices:
        D_random = distance_bin(random_matrix)
        L_random = np.mean(D_random[np.isfinite(D_random)])
        random_path_lengths.append(L_random)
    Lrandom = np.mean(random_path_lengths)
    normalized_path_length = L / Lrandom
    
    return L, normalized_path_length

def calculate_small_world_index(gamma, lambda_):
    sigma = gamma / lambda_
    return sigma

def calculate_efficiency_measures(connectivity_matrix):
    local_efficiency = np.mean(efficiency_bin(connectivity_matrix, local=True))
    global_efficiency = efficiency_bin(connectivity_matrix, local=False)
    return local_efficiency, global_efficiency

def calculate_connectivity_strength(connectivity_matrix):
    strength = np.mean(connectivity_matrix[np.triu_indices_from(connectivity_matrix, k=1)])
    return strength

def calculate_connectivity_diversity(connectivity_matrix):
    N = connectivity_matrix.shape[0]
    mean_pairwise_correlations = np.mean(connectivity_matrix, axis=1)
    connectivity_diversity = np.var(connectivity_matrix - mean_pairwise_correlations[:, None], axis=1)
    average_connectivity_diversity = np.mean(connectivity_diversity)
    return average_connectivity_diversity

def calculate_betweenness_centrality(connectivity_matrix, hippocampal_nodes):
    G = nx.from_numpy_array(connectivity_matrix)
    betweenness = nx.betweenness_centrality(G, normalized=True)
    bc_left = betweenness[hippocampal_nodes['LH']]
    bc_right = betweenness[hippocampal_nodes['RH']]
    return bc_left, bc_right

def generate_random_matrices(connectivity_matrix, num_random_matrices=500):
    random_matrices = []
    for _ in range(num_random_matrices):
        random_matrix = np.random.permutation(connectivity_matrix.flatten()).reshape(connectivity_matrix.shape)
        random_matrices.append(random_matrix)
    return random_matrices

def compute_topological_measures(connectivity_matrix, random_matrices, hippocampal_nodes={'LH':0,'RH':1}):
    # 1. Clustering Coefficients
    C, gamma = calculate_clustering_coefficients(connectivity_matrix, random_matrices)
    # 2. Characteristic Path Length
    L, lambda_ = calculate_characteristic_path_length(connectivity_matrix, random_matrices)
    # 3. Small-World Index
    sigma = calculate_small_world_index(gamma, lambda_)
    # 4. Efficiency Measures
    local_efficiency, global_efficiency = calculate_efficiency_measures(connectivity_matrix)
    # 5. Connectivity Strength
    CS = calculate_connectivity_strength(connectivity_matrix)
    # 6. Connectivity Diversity
    CD = calculate_connectivity_diversity(connectivity_matrix)
    # 7. Betweenness Centrality
    bc_left, bc_right = calculate_betweenness_centrality(connectivity_matrix, hippocampal_nodes)
    
    return {
        'Clustering Coefficient': round(C,3),
        # 'Normalized Clustering Coefficient (gamma)': round(gamma,3),
        'Characteristic Path Length': round(L,3),
        # 'Normalized Characteristic Path Length (lambda)': round(lambda_,3),
        # 'Small-World Index (sigma)': round(sigma,3),
        'Local Efficiency': round(local_efficiency,3),
        # 'Global Efficiency': round(global_efficiency,3),
        'Connectivity Strength': round(CS,3),
        'Connectivity Diversity': round(CD,3),
        # 'Betweenness Centrality (Left Hippocampus)': round(bc_left,3),
        # 'Betweenness Centrality (Right Hippocampus)': round(bc_right,3),
    }
