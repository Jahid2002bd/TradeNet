# src/utils/pattern_learner.py

"""
pattern_learner.py

Trains an unsupervised ML model to detect hidden/anomalous patterns
in market indicator data. Uses DBSCAN clustering to flag rare behaviors.
"""

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class PatternLearner:
    """
    Learns clusters in feature space; identifies noise points as anomalies.
    """

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        """
        Parameters:
            eps (float): Max distance for samples in the same neighborhood.
            min_samples (int): Min samples to form a cluster core.
        """
        self.scaler = StandardScaler()
        self.model = DBSCAN(eps=eps, min_samples=min_samples)

    def fit(self, feature_matrix: np.ndarray) -> None:
        """
        Fit scaler and DBSCAN model on historical feature data.

        Parameters:
            feature_matrix (np.ndarray): Shape (n_samples, n_features).
        """
        scaled_matrix = self.scaler.fit_transform(feature_matrix)
        self.model.fit(scaled_matrix)

    def predict(self, feature_vector: np.ndarray) -> int:
        """
        Predict cluster label for a single feature vector.

        Returns:
            int: Cluster ID; -1 indicates anomaly/noise.
        """
        scaled_vec = self.scaler.transform(feature_vector.reshape(1, -1))
        cluster_id_array = self.model.fit_predict(scaled_vec)
        return int(cluster_id_array[0])

    def detect_anomalies(self, feature_matrix: np.ndarray) -> np.ndarray:
        """
        Identify anomalies in a batch of feature vectors.

        Returns:
            np.ndarray: Array of cluster IDs (-1 for anomalies).
        """
        scaled_matrix = self.scaler.transform(feature_matrix)
        cluster_id_array = self.model.fit_predict(scaled_matrix)
        return cluster_id_array


if __name__ == "__main__":
    # Demo: synthetic data with two clusters + noise
    import numpy as np

    # Sample data: two clusters + noise
    cluster_a = np.random.normal(loc=0.0, scale=1.0, size=(50, 3))
    cluster_b = np.random.normal(loc=5.0, scale=1.0, size=(50, 3))
    noise_data = np.random.uniform(low=-10, high=15, size=(10, 3))
    all_data = np.vstack([cluster_a, cluster_b, noise_data])

    learner = PatternLearner(eps=0.7, min_samples=5)
    learner.fit(all_data)
    anomaly_ids = learner.detect_anomalies(all_data)
    rare_indices = np.where(anomaly_ids == -1)[0].tolist()

    print("Anomalies detected at indices:", rare_indices)
