from sklearn.decomposition import FastICA
from scipy.stats import kurtosis
import numpy as np

def tICA_on_sIC(input_matrix, n_components=10):
    ica = FastICA(n_components=input_matrix.shape[0])
    ica_components = ica.fit_transform(input_matrix.T)

    kurtosis_values = kurtosis(ica_components, axis=0)
    
    top_indices = np.argsort(np.abs(kurtosis_values))[-n_components:][::-1]

    top_ics = ica_components[:, top_indices].T
    top_kurtosis_values = kurtosis_values[top_indices]

    return top_ics, top_kurtosis_values